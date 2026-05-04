import readline  # pyright: ignore[reportUnusedImport] # noqa: F401
import sys

from src.parsing.lexer import lexer
from src.parsing.parse import parser
from src.parsing.tokenizer import tokenizer
from src.tree.debug_tree import print_tree


def repl() -> None:
    """Run the interactive Read Eval Print Loop"""
    while True:
        try:
            user_input = input("\nEnter an equation (or 'q' to quit): ")

            if user_input.strip().lower() in ["q", "quit", "exit"]:
                print("Goodbye!")
                break

            tokens = tokenizer(lexer(user_input))
            for token in tokens:
                print(f"{token.type.name:<12} {token.value}")
            tree = parser(tokens)
            if tree:
                print_tree(tree)

        except SyntaxError as e:
            print(f"SyntaxError: {e}")
        except ValueError as e:
            print(f"ValueError: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
