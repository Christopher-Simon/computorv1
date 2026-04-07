import re
from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    NUMBER = auto()     # "3", "2.5", "3i", "2.5i"
    VARIABLE = auto()   # "x", "varA" — normalized to lowercase
    FUNC_NAME = auto()  # identifier immediately followed by "("
    OPERATOR = auto()   # "+", "-", "*", "**", "/", "^", "%"
    EQUALS = auto()     # "="
    QUERY = auto()      # "?"
    LPAREN = auto()     # "("
    RPAREN = auto()     # ")"
    LBRACKET = auto()   # "["
    RBRACKET = auto()   # "]"
    COMMA = auto()      # "," — column separator in matrix
    SEMICOLON = auto()  # ";" — row separator in matrix


@dataclass
class Token:
    type: TokenType
    value: str


_OPERATORS = {"+", "-", "*", "**", "/", "^", "%"}
_SINGLE_CHAR = {
    "=": TokenType.EQUALS,
    "?": TokenType.QUERY,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    ",": TokenType.COMMA,
    ";": TokenType.SEMICOLON,
}
_NUMBER_PATTERN = re.compile(r"^\d+(?:\.\d+)?i?$")
_I_PREFIX_PATTERN = re.compile(r"^i(\d+(?:\.\d+)?)$")


def lexer(tokens: list[str]) -> list[Token]:
    """
    Classify a flat list of raw string tokens (from tokenizer) into typed Token objects.

    Rules:
    - Numbers (int, float, imaginary suffix 'i') → NUMBER
    - Identifier followed by "(" → FUNC_NAME (normalized lowercase)
    - "i" alone → SyntaxError (reserved imaginary unit, not a variable)
    - Other identifiers → VARIABLE (normalized lowercase)
    - Operators (+, -, *, **, /, ^, %) → OPERATOR
    - Single-char punctuation → their respective type
    """
    result: list[Token] = []
    for i, raw in enumerate(tokens):
        if _NUMBER_PATTERN.match(raw):
            result.append(Token(TokenType.NUMBER, raw))
        elif raw in _OPERATORS:
            result.append(Token(TokenType.OPERATOR, raw))
        elif raw in _SINGLE_CHAR:
            result.append(Token(_SINGLE_CHAR[raw], raw))
        elif raw.isidentifier():
            m = _I_PREFIX_PATTERN.match(raw)
            if m:
                result.append(Token(TokenType.NUMBER, f"{m.group(1)}i"))
                continue
            if raw == "i":
                raise SyntaxError(
                    "'i' is reserved for the imaginary unit "
                    "and cannot be used as a variable"
                )
            normalized = raw.lower()
            next_tok = tokens[i + 1] if i + 1 < len(tokens) else None
            if next_tok == "(":
                result.append(Token(TokenType.FUNC_NAME, normalized))
            else:
                result.append(Token(TokenType.VARIABLE, normalized))
        else:
            raise SyntaxError(f"Unexpected token: {raw!r}")
    return result
