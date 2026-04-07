In the tree

**operators** (these are nodes)
absctract class with compute method
each overload the compute method

+ (addition)
- (substraction)
/ (division)
* (multiplication)
** (matrix multiplication)
^ (power)
% (modulo)


These are leafs
**Operands**
absctract class with get_value()
each class compute to update the value


Not sure of implementation of each (espcially functions and matrices)

*Matrices*
[[2,3];[4,3]] (infinite depth)
MatrixNode
rows : list[MatrixNode]

*Functions*
fun_name(argument)

*Rational*
RationalType
value: float

*Imaginary*
ImaginaryType:
Value: float
 # Only imaginary or complex (real + imaginary)?

*Variable*
a-zA-Z
value : TreeNode

Used for lexer only :

**Seperators**
()
= -> should be treated to simplify the equation (=0) or value assignment



Operator = ADD, SUB, DIV, MUL, MOD, DOT, POW
Operand = RATIONAL, IMAGINARY, MatrixNode, FUNC, VAR

```python
class TreeNode:
    value : Operator | Operand
    left: TreeNode | None
    right: TreeNode | None
    if operand:
        left = None
        right = None
```

```python
class MatrixNode:
    value: List[TreeNode]

    def __post_init__(self) -> None:
    if not self.value:
        raise ValueError("Empty MatrixNode")
    has_matrix = any(isinstance(e, MatrixNode) for e in self.value)
    if has_matrix:
        if not all(isinstance(e, MatrixNode) for e in self.value):
            raise ValueError("Mixed MatrixNode and TreeNode in same level")
        lengths = {len(e.value) for e in self.value}  # type: ignore[union-attr]
        if len(lengths) != 1:
            raise ValueError("Rows must all be the same length")
```

Tensors vs Matrix 



| Dimensions | Common Name     | Programming Name | Tensor Rank |
|------------|-----------------|------------------|-------------|
| 0D         | Scalar / Number | int or float     | Rank 0      |
| 1D         | Vector / List   | array            | Rank 1      |
| 2D         | Matrix          | 2D array         | Rank 2      |
| 3D         | Tensor          | 3D array         | Rank 3      |
| nD         | Tensor          | nD array         | Rank n      |


Operations that generalize cleanly (element-wise)
+, -, %, scalar * — same rule at any depth: same shape required, apply recursively to each leaf.


A(2×3×4) + B(2×3×4) → recurse down, add scalars at depth 3
Your operator's compute() just recurses through MatrixNode levels uniformly.

Operations that diverge
* (element-wise matrix multiplication) — same as above, works for tensors.

** (dot product / matmul) — this is where it breaks:

2D: A(m×n) ** B(n×p) → (m×p), contracts the inner dimension
Tensors: operates on the last two dimensions, broadcasts over the rest — batched matmul

A(2×3×4) ** B(2×4×5) → (2×3×5)   ← not the same rule
^ (power) — for 2D means repeated ** (square matrix only). For tensors, even more ambiguous — applies per-matrix in the batch? Undefined in general.

