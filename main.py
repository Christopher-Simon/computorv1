"""
Predict module for the application.
"""

import sys


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

            print("User input:", user_input)

        except ValueError:
            print("Invalid input. Please enter a numerical value.")
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)


if __name__ == "__main__":
    main()