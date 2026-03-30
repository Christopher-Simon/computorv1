import re


def identifier(input: str) -> list[str]:
    pattern = re.compile(r"\d+(?:\.\d*)?|[+\-*/^()]")
    result = re.findall(pattern, input)
    print(result)
    return result
