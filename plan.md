# Computorv1 & v2 — Implementation Plan

## Build Order

### Step 1 — Fix tokenizer (`src/tokenizer.py`)

Add missing tokens to the regex pattern:
- `;` — matrix row separator
- `%` — modulo operator  
- `?` — resolution trigger (`a + 2 = ?`)

New pattern:
```python
r"\*\*|\d+(?:\.\d+)?i?|[a-zA-Z_]\w*\([^)]*\)|[a-zA-Z_]\w*|[=+\-*/^()\[\],;%?]"
```

Also fix `main.py` line 24-26: capture `tokenizer()` result and iterate over it.

**Tests** (`tests/test_tokenizer.py`):
- `"5 * X^2 + 4 * X^1"` → correct token list
- `"[[1,2];[3,4]]"` → `;` present
- `"a + 2 = ?"` → `?` present
- `"4 % 2"` → `%` present
- imaginary: `"3i"`, `"2.5i"`
- function call: `"funA(x)"`

---

### Step 2 — AST data structures (`src/ast.py`)

```python
class Operator(Enum):
    ADD, SUB, MUL, DIV, MOD, DOT, POW

@dataclass
class Rational:
    value: float

@dataclass  
class Imaginary:
    value: float   # coefficient of i only

@dataclass
class Variable:
    name: str      # looked up in env at eval time

@dataclass
class FuncCall:
    name: str
    arg: "TreeNode"

@dataclass
class FunctionDef:       # stored in env, not in the tree
    param: str
    body: "TreeNode"

Operand = Rational | Imaginary | Variable | FuncCall | MatrixNode

@dataclass
class TreeNode:
    value: Operator | Operand
    left: "TreeNode | None" = None
    right: "TreeNode | None" = None
    # __post_init__: validate left/right are None iff value is Operand

@dataclass
class MatrixNode:
    value: list["MatrixNode"] | list[TreeNode]
    # __post_init__: shape validation
    def shape(self) -> tuple[int, ...]: ...  # recursive
    # Rules:
    # - not empty
    # - if any element is MatrixNode, ALL must be MatrixNode
    # - all sibling MatrixNodes must have same shape()
```

**Tests** (`tests/test_ast.py`):
- `MatrixNode` valid 2×2
- unequal row lengths → raises
- mixed MatrixNode + TreeNode → raises
- `shape()` returns `(2, 2)` for 2×2, `(2, 3, 4)` for 3D tensor

---

### Step 3 — Lexer (`src/lexer.py`)

Classifies `list[str]` → `list[Token]`. Annotates type only, does NOT build tree.

```python
class TokenType(Enum):
    NUMBER      # "3", "2.5", "3i", "2.5i"
    VARIABLE    # "x", "vara" (normalized lowercase)
    FUNC_NAME   # identifier followed by "("
    OPERATOR    # "+", "-", "*", "**", "/", "^", "%"
    EQUALS      # "="
    QUERY       # "?"
    LPAREN, RPAREN
    LBRACKET, RBRACKET
    COMMA       # "," column separator
    SEMICOLON   # ";" row separator

@dataclass
class Token:
    type: TokenType
    value: str
```

Key rules:
- `"i"` alone → **raises SyntaxError** (reserved, cannot be a variable name)
- All identifiers normalized to lowercase (`varA` → `vara`)
- `"**"` → OPERATOR, `"*"` → OPERATOR (tokenizer handles ordering)
- identifier followed by `"("` → FUNC_NAME, else VARIABLE

**Tests** (`tests/test_lexer.py`):
- `"3i"` → `Token(NUMBER, "3i")`
- `"i"` alone → raises `SyntaxError`
- `"varA"` → `Token(VARIABLE, "vara")` (normalized)
- `"funA"` followed by `"("` → `Token(FUNC_NAME, "funa")`
- `"**"` → `Token(OPERATOR, "**")`

---

### Step 4 — Parser (`src/parser.py`)

Takes `list[Token]` → `TreeNode`. Recursive descent.

Precedence (low → high):
1. `=` / `?` (statement level)
2. `+` `-`
3. `*` `/` `%` `**`
4. `^` (right-associative)
5. unary `-`
6. atoms: number, variable, `funA(expr)`, `(expr)`, `[[...]]`

`=` disambiguation by LHS shape:
- `NAME "(" NAME ")"` on LHS → FunctionDef
- `expr` on LHS, `?` on RHS → query
- `expr` on LHS, `expr` on RHS → equation to solve

**Tests** (`tests/test_parser.py`):
- `"2 + 3 * 4"` → mul binds tighter than add
- `"x^2"` → `POW(Variable(x), Rational(2))`
- `"funA(x) = 2*x + 1"` → FunctionDef
- `"a + 2 = ?"` → query node
- `"[[1,2];[3,4]]"` → MatrixNode(2×2)
- v1 mandatory examples (see Step 6)

---

### Step 5 — Evaluator (`src/evaluator.py`)

Takes `TreeNode` + `Env` → reduced `TreeNode`.

```python
Env = dict[str, TreeNode | FunctionDef]

def evaluate(node: TreeNode, env: Env) -> TreeNode: ...
def substitute(node: TreeNode, param: str, arg: TreeNode) -> TreeNode: ...
```

Operator type compatibility:
| Op  | Rational | Imaginary | Matrix |
|-----|----------|-----------|--------|
| +/- | ✓ | ✓ complex emerges | ✓ same shape |
| *   | ✓ | ✓ | ✓ scalar×mat or same-shape element-wise |
| **  | ✗ | ✗ | ✓ A(m×n)**B(n×p) |
| ^   | ✓ int exp | ✗ | ✗ |
| %   | ✓ | ✗ | ✗ |

Incompatible types → raise `TypeError`.

**Tests** (`tests/test_evaluator.py`):
- `2 + 3` → `Rational(5)`
- `3 + 2i` → complex result
- matrix add same shape → ok; different shape → raises
- `(2×3) ** (3×2)` → `(2×2)`
- `funA(3)` with `funA(x) = 2*x` → `Rational(6)`
- unknown variable → raises `NameError`

---

### Step 6 — v1 Solver (`src/solver.py`)

Reduces equation to 0, extracts polynomial coefficients, solves degree ≤ 2.

```python
def collect_terms(node: TreeNode) -> dict[int, float]: ...
def solve(lhs: TreeNode, rhs: TreeNode) -> str: ...
```

Output: reduced form, degree, discriminant sign, solutions.

**Tests** (`tests/test_solver.py`) — subject examples verbatim:
- `5*X^0 + 4*X^1 - 9.3*X^2 = 1*X^0` → degree 2, disc>0, {0.905239, -0.475131}
- `5*X^0 + 4*X^1 = 4*X^0` → degree 1, -0.25
- `8*X^0 - 6*X^1 + 0*X^2 - 5.6*X^3 = 3*X^0` → degree 3, can't solve
- `6*X^0 = 6*X^0` → all reals
- `10*X^0 = 15*X^0` → no solution
- `1*X^0 + 2*X^1 + 5*X^2 = 0` → degree 2, disc<0, complex solutions

---

### Step 7 — Wire up `main.py`

- v1 mode: `python main.py "5 * X^0 + 4 * X^1 = 4 * X^0"` (CLI arg)
- v2 mode: REPL loop, `Env` persists across inputs

---

## Critical Files

| File | Role |
|------|------|
| `src/tokenizer.py` | Fix: add `;` `%` `?` |
| `src/ast.py` | New: all node types |
| `src/lexer.py` | Rewrite: Token + lexer() |
| `src/parser.py` | New: recursive descent |
| `src/evaluator.py` | New: tree reduction + env |
| `src/solver.py` | New: v1 polynomial solver |
| `main.py` | Fix bug + wire pipeline |
| `tests/test_*.py` | New: one file per stage |

---

## Verification

```bash
pytest
mypy src/
ruff check src/

# v1 subject examples
python main.py "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"
python main.py "5 * X^0 + 4 * X^1 = 4 * X^0"
python main.py "8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0"
python main.py "6 * X^0 = 6 * X^0"
python main.py "10 * X^0 = 15 * X^0"
python main.py "1 * X^0 + 2 * X^1 + 5 * X^2 = 0"
```
