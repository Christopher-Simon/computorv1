from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Operator(Enum):
    ADD = "+"
    SUB = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    DOT = "**"  # matrix multiplication
    POW = "^"  # scalar power


@dataclass
class Rational:
    value: float


@dataclass
class Imaginary:
    value: float  # coefficient of i


@dataclass
class Variable:
    name: str  # normalized lowercase; looked up in env at eval time


@dataclass
class FuncCall:
    name: str  # normalized lowercase
    arg: TreeNode


@dataclass
class FunctionDef:
    param: str  # normalized lowercase
    body: TreeNode


@dataclass
class MatrixNode:
    value: list[MatrixNode] | list[TreeNode]

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("MatrixNode cannot be empty")
        has_matrix = any(isinstance(e, MatrixNode) for e in self.value)
        if has_matrix:
            if not all(isinstance(e, MatrixNode) for e in self.value):
                raise ValueError("Mixed MatrixNode and TreeNode in same level")
            nested = [e for e in self.value if isinstance(e, MatrixNode)]
            shapes = {e.shape() for e in nested}
            if len(shapes) != 1:
                raise ValueError("All nested MatrixNodes must have the same shape")

    def shape(self) -> tuple[int, ...]:
        """
        Return the shape of this tensor as a tuple of dimension sizes.

        A flat row of n TreeNodes returns (n,).
        A matrix of r rows, each with c elements, returns (r, c).
        Nesting is recursive: a 2×3×4 tensor returns (2, 3, 4).
        """
        n = len(self.value)
        first = self.value[0]
        if isinstance(first, MatrixNode):
            return (n, *first.shape())
        return (n,)


Operand = Rational | Imaginary | Variable | FuncCall | MatrixNode


@dataclass
class TreeNode:
    value: Operator | Operand
    left: TreeNode | None = field(default=None)
    right: TreeNode | None = field(default=None)

    def __post_init__(self) -> None:
        if isinstance(self.value, Operand):
            if self.left is not None or self.right is not None:
                raise ValueError("Operand nodes must have left=None and right=None")
