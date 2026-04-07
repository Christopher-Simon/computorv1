import re
from collections.abc import Iterator


def tokenizer(input: str) -> list[str]:
    """
    Regex function to return list of identified parts of polynomial expressions
    """
    pattern = re.compile(r"\*\*|\d+(?:\.\d+)?i?|[a-zA-Z_]\w*|[=+\-*/^()\[\],;%?]")
    results: Iterator[re.Match[str]] = re.finditer(pattern, input)
    return [result.group() for result in results]
