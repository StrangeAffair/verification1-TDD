# pylint: disable=R0801
"""Parser implementation"""
import unittest
import os
from abc import ABC, abstractmethod
from fractions import Fraction
from Token import Token
from Token import TokenPlus, TokenMinus, TokenMultiply, TokenDivision
from Token import TokenLParenthese, TokenRParenthese


class Expression(ABC):  # pylint: disable=R0903
    """Base expression class"""
    @abstractmethod
    def Evaluate(self) -> Fraction:
        """virtual method, which should return expression result"""


class NumberExpression(Expression):  # pylint: disable=R0903
    """Expression class for numbers"""
    def __init__(self, number):
        self.number = number

    def Evaluate(self) -> Fraction:
        """virtual method, which should return expression result"""
        return Fraction(self.number)


class UnaryExpression(Expression):  # pylint: disable=R0903
    """Expression class for unary operators"""
    def __init__(self, right: Expression, operation: Token):
        self.right     = right      # noqa: E221
        self.operation = operation

    def Evaluate(self) -> Fraction:
        """virtual method, which should return expression result"""
        if self.operation == TokenPlus():
            return +self.right.Evaluate()
        if self.operation == TokenMinus():
            return -self.right.Evaluate()

        raise RuntimeError("UnaryExpression: bad operation", self.operation)


class BinaryExpression(Expression):  # pylint: disable=R0903
    """Expression class for binary operators"""
    def __init__(self, left: Expression, right: Expression, operation: Token):
        self.left      = left       # noqa: E221
        self.right     = right      # noqa: E221
        self.operation = operation

    def Evaluate(self) -> Fraction:
        """virtual method, which should return expression result"""
        if self.operation == TokenPlus():
            return self.left.Evaluate() + self.right.Evaluate()
        if self.operation == TokenMinus():
            return self.left.Evaluate() - self.right.Evaluate()
        if self.operation == TokenMultiply():
            return self.left.Evaluate() * self.right.Evaluate()
        if self.operation == TokenDivision():
            return self.left.Evaluate() / self.right.Evaluate()

        raise RuntimeError("BinaryExpression: bad operation", self.operation)


class Parser:
    """Parser class"""
    def __init__(self, tokens: list[Token]):
        self.tokens   = tokens  # noqa: E221
        self.position = 0

    def PeekToken(self, offset: int = 0) -> Token | None:
        """returns token at current position + offset or None"""
        if self.position + offset >= len(self.tokens):
            return None
        return self.tokens[self.position + offset]

    def NextToken(self) -> Token | None:
        """returns next token or None"""
        self.position += 1
        return self.PeekToken()

    def Parse(self) -> Expression:
        """parse file"""
        return self.Additive()

    def Additive(self) -> Expression:
        """parse additive expression"""
        retval = self.Multiplicative()

        while True:
            token = self.PeekToken()
            if token is None:
                return retval
            if token == TokenPlus():
                self.NextToken()
                retval = BinaryExpression(retval, self.Unary(), TokenPlus())
                continue
            if token == TokenMinus():
                self.NextToken()
                retval = BinaryExpression(retval, self.Unary(), TokenMinus())
                continue
            break

        return retval

    def Multiplicative(self) -> Expression:
        """parse multiplicative expression"""
        retval = self.Unary()

        while True:
            token = self.PeekToken()
            if token is None:
                return retval
            if token == TokenMultiply():
                self.NextToken()
                right = self.Unary()
                retval = BinaryExpression(retval, right, TokenMultiply())
                continue
            if token == TokenDivision():
                self.NextToken()
                right = self.Unary()
                retval = BinaryExpression(retval, right, TokenDivision())
                continue
            break

        return retval

    def Unary(self) -> Expression:
        """parse unary expression [+expr, -expr]"""
        token = self.PeekToken()
        if token == TokenPlus():
            self.NextToken()
            return UnaryExpression(self.Primary(), TokenPlus())
        if token == TokenMinus():
            self.NextToken()
            return UnaryExpression(self.Primary(), TokenMinus())

        return self.Primary()

    def Primary(self) -> Expression:
        """parse primary expression [number, (...)]"""
        token = self.PeekToken()
        if token is None:
            raise RuntimeError("expected token not None in primary")
        if token.type == "Number":
            self.NextToken()
            return NumberExpression(token.data)
        if token == TokenLParenthese():
            self.NextToken()
            expr = self.Additive()

            token = self.PeekToken()
            assert token == TokenRParenthese()
            self.NextToken()
            return expr

        raise RuntimeError("error token in primary", token)


class ParserTestCase(unittest.TestCase):
    """Parser test class"""
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

            array = eval(lines[1].strip())  # pylint: disable=W0123
            for index, element in enumerate(array):
                array[index] = Token.FromString(element)

            parser = Parser(array)
            result = parser.Parse()
            actual = result.Evaluate()

            expected = lines[3].strip()
            expected = eval(expected)  # pylint: disable=W0123
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    this_file_directory = os.path.dirname(__file__)
    base_directory = os.path.join(this_file_directory, '..')
    base_directory = os.path.normpath(base_directory)
    tests_directory = os.path.join(base_directory, 'tests', 'parser')

    suite = unittest.TestSuite()
    with os.scandir(tests_directory) as iterator:
        for entity in iterator:
            if entity.is_file():
                suite.addTest(ParserTestCase("TestFile", entity.path))

    unittest.TextTestRunner(verbosity=2).run(suite)
