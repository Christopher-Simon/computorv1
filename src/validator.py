import re


def validator(input: str) -> str:
    """
    Function to validate the input.

    If the user input contains something other than.
    X, ^, a digit. raise
    """
    if not re.fullmatch(r'[Xx\+\-\*\/\^\d\s()]+', input):
        raise ValueError(f"Invalid input: '{input}'. Only 'X', 'x', '^', and digits are allowed.")
    return input

