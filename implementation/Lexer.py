import unittest
import os
from Token import *

class Lexer:
    def __init__(self, string: str):
        self.file     = string
        self.line     = 1
        self.column   = 0
        self.position = 0
    
    def PeekChar(self, offset: int = 0) -> str:
        if self.position + offset >= len(self.file):
            return "\0"
        return self.file[self.position + offset]
    
    def NextChar(self) -> str:
        if self.PeekChar() == '\n':
            self.line   += 1
            self.column =  0
        else:
            self.column += 1
        
        self.position += 1
        return self.PeekChar()
    
    def TokenizeNumber(self):
        number = 0
        char   = self.PeekChar()
        while char.isdigit():
            number = number * 10 + int(char)
            char   = self.NextChar()
        
        return number
    
    def NextToken(self):
        char = self.PeekChar()
        while char.isspace():
            char = self.NextChar()

        if not char.isprintable():
            return None

        # pre save
        line   = self.line
        column = self.column
        if char.isdigit():
            data   = self.TokenizeNumber()
            return Token("Number", data, line, column)

        if char == '+':
            self.NextChar()
            return TokenPlus(line, column)
        if char == '-':
            self.NextChar()
            return TokenMinus(line, column)

        if char == '(':
            self.NextChar()
            return TokenLParenthese(line, column)
        if char == ')':
            self.NextChar()
            return TokenRParenthese(line, column)

        return None

    def Tokens(self):
        result = []
        while True:
            token = self.NextToken()
            if token is None:
                break
            result.append(token)
        return result

class LexerTestCase(unittest.TestCase):
    def __init__(self, testName, path):
        super(LexerTestCase, self).__init__(testName)
        self.path = path

    def test_file(self):
        print(self.path)
        with open(self.path, "r") as file:
            lines = file.readlines()
            self.assertEqual(lines[0], "input:\n")
            self.assertEqual(lines[2], "output:\n")
            
            lexer  = Lexer(lines[1])
            result = lexer.Tokens()
            self.assertEqual(str(result), lines[3][:-1])

if __name__ == "__main__":
    suite = unittest.TestSuite()
    with os.scandir("../tests/lexer") as iterator:
        for entity in iterator:
            if entity.is_file():    
                suite.addTest(LexerTestCase("test_file", entity.path))
    
    unittest.TextTestRunner(verbosity=2).run(suite)