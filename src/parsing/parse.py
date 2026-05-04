from src.parsing.tokenizer import Token, TokenType
from src.tree.ast import Operator, Rational, TreeNode


class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current = 0

    def _peek(self) -> Token:
        return self.tokens[self.current]

    def _previous(self) -> Token:
        return self.tokens[self.current - 1]

    def _next(self) -> Token:
        return self.tokens[self.current + 1]

    def _advance(self):
        self.current += 1

    def _expression(self) -> TreeNode | None:
        if self._next().type == TokenType.OPERATOR:
            self._advance
            return TreeNode(
                Operator(self._peek().value),
                left=TreeNode(Rational(float(self._previous().value))),
                right=TreeNode(Rational(float(self._next().value))),
            )

    def parse(self) -> TreeNode | None:
        return self._expression()
