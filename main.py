"""
Predict module for the application.
"""

import readline  # pyright: ignore[reportUnusedImport] # noqa: F401
import sys

from src.lexer import lexer
from src.tokenizer import tokenizer


def main() -> None:
    print("=========================================")
    print("                Computor V1              ")
    print("=========================================")

    while True:
        try:
            user_input = input("\nEnter an equation (or 'q' to quit): ")

            if user_input.strip().lower() in ["q", "quit", "exit"]:
                print("Goodbye!")
                break

            tokens = lexer(tokenizer(user_input))
            for token in tokens:
                print(f"{token.type.name:<12} {token.value}")

        except ValueError:
            print("Invalid input. Please enter a numerical value.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)


if __name__ == "__main__":
    main()
