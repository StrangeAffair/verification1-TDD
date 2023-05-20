# pylint: disable=C0103,R0801,W0621
"""primitive calculator"""
import unittest
import os
from fractions import Fraction  # noqa: F401 # pylint: disable=W0611
from Lexer import Lexer
from Parser import Parser


class FullTestCase(unittest.TestCase):
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

            lexer  = Lexer(lines[1].strip())  # noqa: E221
            parser = Parser(lexer.Tokens())
            result = parser.Parse()
            actual = result.Evaluate()

            expected = lines[3].strip()
            expected = eval(expected)  # pylint: disable=W0123
            self.assertEqual(actual, expected)


if __name__ == "__main__":
    this_file_directory = os.path.dirname(__file__)
    base_directory = os.path.join(this_file_directory, '..')
    base_directory = os.path.normpath(base_directory)
    tests_directory = os.path.join(base_directory, 'tests', 'full')

    suite = unittest.TestSuite()
    with os.scandir(tests_directory) as iterator:
        for entity in iterator:
            if entity.is_file():
                suite.addTest(FullTestCase("TestFile", entity.path))

    unittest.TextTestRunner(verbosity=2).run(suite)

INTERACTIVE = False
if INTERACTIVE:
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
