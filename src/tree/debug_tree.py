from __future__ import annotations

from src.tree.ast import (
    FuncCall,
    Imaginary,
    MatrixNode,
    Operator,
    Rational,
    TreeNode,
    Variable,
)


def _fmt(v: float) -> str:
    return str(int(v)) if v == int(v) else str(v)


def _node_info(node: TreeNode) -> tuple[str, list[TreeNode | MatrixNode]]:
    v = node.value
    if isinstance(v, Operator):
        label = ("unary " if node.left is None else "") + v.value
        children: list[TreeNode | MatrixNode] = []
        if node.left is not None:
            children.append(node.left)
        if node.right is not None:
            children.append(node.right)
        return label, children
    if isinstance(v, Rational):
        return _fmt(v.value), []
    if isinstance(v, Imaginary):
        return f"{_fmt(v.value)}i", []
    if isinstance(v, Variable):
        return v.name, []
    if isinstance(v, FuncCall):
        return f"{v.name}(...)", [v.arg]
    if isinstance(v, MatrixNode):
        return f"Matrix{v.shape()}", list(v.value)  # type: ignore[arg-type]
    return repr(v), []


def _render(node: TreeNode | MatrixNode, prefix: str, is_last: bool) -> None:
    connector = "└── " if is_last else "├── "
    child_prefix = prefix + ("    " if is_last else "│   ")

    if isinstance(node, MatrixNode):
        print(prefix + connector + f"Matrix{node.shape()}")
        items = list(node.value)
        for i, child in enumerate(items):
            _render(child, child_prefix, i == len(items) - 1)
    else:
        label, children = _node_info(node)
        print(prefix + connector + label)
        for i, child in enumerate(children):
            _render(child, child_prefix, i == len(children) - 1)


def print_tree(node: TreeNode) -> None:
    """Print a visual representation of the AST rooted at *node*."""
    label, children = _node_info(node)
    print(label)
    for i, child in enumerate(children):
        _render(child, "", i == len(children) - 1)
