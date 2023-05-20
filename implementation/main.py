# pylint: disable=C0103
"""primitive calculator"""
from Lexer import Lexer
from Parser import Parser

if __name__ == "__main__":
    while True:
        string = input("Enter expression:\n")
        if string == "":
            continue
        if string in ["exit", "quit"]:
            break
        lexer  = Lexer(string)  # noqa: E221
        parser = Parser(lexer.Tokens())
        result = parser.Parse().Evaluate()
        print(result)
