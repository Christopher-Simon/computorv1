from src.parsing.lexer import lexer as tokenizer


def test_basic_polynomial() -> None:
    assert tokenizer("5 * X^2 + 4 * X^1") == [
        "5",
        "*",
        "X",
        "^",
        "2",
        "+",
        "4",
        "*",
        "X",
        "^",
        "1",
    ]


def test_matrix_semicolon() -> None:
    tokens = tokenizer("[[1,2];[3,4]]")
    assert ";" in tokens


def test_query_operator() -> None:
    tokens = tokenizer("a + 2 = ?")
    assert "?" in tokens


def test_modulo() -> None:
    tokens = tokenizer("4 % 2")
    assert "%" in tokens


def test_imaginary_integer() -> None:
    assert tokenizer("3i") == ["3i"]


def test_imaginary_float() -> None:
    assert tokenizer("2.5i") == ["2.5i"]


def test_imaginary_in_expression() -> None:
    tokens = tokenizer("2*i + 3")
    assert tokens == ["2", "*", "i", "+", "3"]


def test_matrix_full() -> None:
    assert tokenizer("[[1,2];[3,4]]") == [
        "[",
        "[",
        "1",
        ",",
        "2",
        "]",
        ";",
        "[",
        "3",
        ",",
        "4",
        "]",
        "]",
    ]


def test_dot_product() -> None:
    tokens = tokenizer("A ** B")
    assert "**" in tokens
    assert "*" not in tokens


def test_v1_mandatory_example() -> None:
    tokens = tokenizer("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
    assert "=" in tokens
    assert "9.3" in tokens


def test_function_call() -> None:
    tokens = tokenizer("funA(x)")
    assert "funA" in tokens
    assert "(" in tokens
    assert "x" in tokens
    assert ")" in tokens


def test_empty_string() -> None:
    assert tokenizer("") == []


def test_whitespace_ignored() -> None:
    assert tokenizer("  3  +  4  ") == ["3", "+", "4"]
