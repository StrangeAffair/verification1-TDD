"""Lexer implementation"""
import unittest
import os
from Token import Token
from Token import TokenPlus, TokenMinus, TokenMultiply, TokenDivision
from Token import TokenLParenthese, TokenRParenthese


class Lexer:
    """Lexer class"""
    def __init__(self, string: str):
        self.file     = string  # noqa: E221
        self.line     = 1  # noqa: E221
        self.column   = 0  # noqa: E221
        self.position = 0  # noqa: E221

    def PeekChar(self, offset: int = 0) -> str:
        """returns char at current position + offset or '\0'"""
        if self.position + offset >= len(self.file):
            return "\0"
        return self.file[self.position + offset]

    def NextChar(self) -> str:
        """returns next char or '\0'"""
        if self.PeekChar() == '\n':
            self.line   += 1  # noqa: E221, E222
            self.column =  0  # noqa: E221, E222
        else:
            self.column += 1  # noqa: E221, E222

        self.position += 1
        return self.PeekChar()

    def TokenizeNumber(self):
        """scans string for number"""
        number = 0
        char   = self.PeekChar()  # noqa: E221
        while char.isdigit():
            number = number * 10 + int(char)
            char   = self.NextChar()  # noqa: E221

        return number

    def NextToken(self):  # pylint: disable=R0911
        """returns next token from string"""
        char = self.PeekChar()
        while char.isspace():
            char = self.NextChar()

        if not char.isprintable():
            return None

        # pre save
        line   = self.line    # noqa: E221
        column = self.column  # noqa: E221
        if char.isdigit():
            data = self.TokenizeNumber()
            return Token("Number", data, line, column)

        if char == '+':
            self.NextChar()
            return TokenPlus(line, column)
        if char == '-':
            self.NextChar()
            return TokenMinus(line, column)
        if char == '*':
            self.NextChar()
            return TokenMultiply(line, column)
        if char == '/':
            self.NextChar()
            return TokenDivision(line, column)

        if char == '(':
            self.NextChar()
            return TokenLParenthese(line, column)
        if char == ')':
            self.NextChar()
            return TokenRParenthese(line, column)

        return None

    def Tokens(self):
        """returns list of tokens for string"""
        result = []
        while True:
            token = self.NextToken()
            if token is None:
                break
            result.append(token)
        return result


class LexerTestCase(unittest.TestCase):
    """Lexer test class"""
    def __init__(self, testName, path):
        super().__init__(testName)
        self.path = path

    def TestFile(self):
        """do a test from file"""
        print(self.path)
        with open(self.path, encoding="utf-8") as file:
            lines = file.readlines()
            self.assertEqual(lines[0].strip(), "input:")
            self.assertEqual(lines[2].strip(), "output:")

            lexer  = Lexer(lines[1])  # noqa: E221
            result = lexer.Tokens()
            self.assertEqual(str(result), lines[3].strip())


if __name__ == "__main__":
    suite = unittest.TestSuite()
    with os.scandir("../tests/lexer") as iterator:
        for entity in iterator:
            if entity.is_file():
                suite.addTest(LexerTestCase("TestFile", entity.path))

    unittest.TextTestRunner(verbosity=2).run(suite)
