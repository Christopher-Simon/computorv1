import pytest

from src.parsing.tokenizer import Token, TokenType, tokenizer as lexer

# --- numbers ---


def test_integer() -> None:
    assert lexer(["42"]) == [Token(TokenType.NUMBER, "42")]


def test_float() -> None:
    assert lexer(["3.14"]) == [Token(TokenType.NUMBER, "3.14")]


def test_imaginary_suffix() -> None:
    assert lexer(["3i"]) == [Token(TokenType.NUMBER, "3i")]


def test_imaginary_float_suffix() -> None:
    assert lexer(["2.5i"]) == [Token(TokenType.NUMBER, "2.5i")]


def test_imaginary_prefix_form() -> None:
    # "i3" → rewritten to "3i"
    assert lexer(["i3"]) == [Token(TokenType.NUMBER, "3i")]


def test_imaginary_prefix_float_form_raises() -> None:
    # "i2.5" is not a valid identifier, so it hits the unexpected-token branch
    with pytest.raises(SyntaxError):
        lexer(["i2.5"])


# --- reserved 'i' / 'I' ---


def test_bare_i_raises() -> None:
    with pytest.raises(SyntaxError):
        lexer(["i"])


def test_bare_cap_i_raises() -> None:
    with pytest.raises(SyntaxError):
        lexer(["I"])


# --- variables ---


def test_variable_lowercase() -> None:
    assert lexer(["x"]) == [Token(TokenType.VARIABLE, "x")]


def test_variable_normalized_to_lowercase() -> None:
    assert lexer(["X"]) == [Token(TokenType.VARIABLE, "x")]


def test_variable_mixed_case_normalized() -> None:
    assert lexer(["VarA"]) == [Token(TokenType.VARIABLE, "vara")]


# --- function names ---


def test_func_name_before_lparen() -> None:
    assert lexer(["funA", "("]) == [
        Token(TokenType.FUNC_NAME, "funa"),
        Token(TokenType.LPAREN, "("),
    ]


def test_identifier_without_lparen_is_variable() -> None:
    assert lexer(["funA"]) == [Token(TokenType.VARIABLE, "funa")]


# --- operators ---


def test_operators() -> None:
    for op in ("+", "-", "*", "**", "/", "^", "%"):
        assert lexer([op]) == [Token(TokenType.OPERATOR, op)]


# --- single-char punctuation ---


def test_equals() -> None:
    assert lexer(["="]) == [Token(TokenType.EQUALS, "=")]


def test_query() -> None:
    assert lexer(["?"]) == [Token(TokenType.QUERY, "?")]


def test_parens() -> None:
    assert lexer(["(", ")"]) == [
        Token(TokenType.LPAREN, "("),
        Token(TokenType.RPAREN, ")"),
    ]


def test_brackets() -> None:
    assert lexer(["[", "]"]) == [
        Token(TokenType.LBRACKET, "["),
        Token(TokenType.RBRACKET, "]"),
    ]


def test_comma() -> None:
    assert lexer([","]) == [Token(TokenType.COMMA, ",")]


def test_semicolon() -> None:
    assert lexer([";"]) == [Token(TokenType.SEMICOLON, ";")]


# --- unexpected token ---


def test_unexpected_token_raises() -> None:
    with pytest.raises(SyntaxError):
        lexer(["@"])


# --- full expression ---


def test_polynomial_expression() -> None:
    tokens = lexer(["5", "*", "X", "^", "2", "+", "4", "*", "X", "^", "1", "=", "0"])
    assert tokens == [
        Token(TokenType.NUMBER, "5"),
        Token(TokenType.OPERATOR, "*"),
        Token(TokenType.VARIABLE, "x"),
        Token(TokenType.OPERATOR, "^"),
        Token(TokenType.NUMBER, "2"),
        Token(TokenType.OPERATOR, "+"),
        Token(TokenType.NUMBER, "4"),
        Token(TokenType.OPERATOR, "*"),
        Token(TokenType.VARIABLE, "x"),
        Token(TokenType.OPERATOR, "^"),
        Token(TokenType.NUMBER, "1"),
        Token(TokenType.EQUALS, "="),
        Token(TokenType.NUMBER, "0"),
    ]


def test_matrix_tokens() -> None:
    tokens = lexer(["[", "[", "1", ",", "2", "]", ";", "[", "3", ",", "4", "]", "]"])
    assert tokens[0] == Token(TokenType.LBRACKET, "[")
    assert Token(TokenType.SEMICOLON, ";") in tokens
    assert Token(TokenType.COMMA, ",") in tokens


def test_empty_input() -> None:
    assert lexer([]) == []
