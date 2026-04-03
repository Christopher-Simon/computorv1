

from dataclasses import dataclass
from enum import Enum

class TokenType(Enum):
    Rational = 1
    Imaginary = 2
    Matrices = 3
    Functions = 4
    Variable = 5


@dataclass
class Token():


def lexer(inputs: list[str]) -> None:
    """
    Transform inputs into token
    Return is yet to be defined
    """

    pass
