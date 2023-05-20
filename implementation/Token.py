"""Token implementation"""


class Token:
    """Input element for parser"""
    def __init__(self,
                 type:   str,  # pylint: disable=W0622
                 data:   int | None = None,
                 line:   int | None = None,
                 column: int | None = None):
        self.type   = type  # noqa: E221
        self.data   = data  # noqa: E221
        self.line   = line  # noqa: E221
        self.column = column

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if self.data is None:
            return f"{self.type}"

        return f"{self.type}({self.data})"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.type == other

        return (self.type == other.type) and (self.data == other.data)

    @staticmethod
    def FromString(string):  # pylint: disable=R0911
        """get Token from string"""
        string = string.strip()
        if string == "Plus":
            return TokenPlus()
        if string == "Minus":
            return TokenMinus()
        if string == "Multiply":
            return TokenMultiply()
        if string == "Division":
            return TokenDivision()

        if string == "LParenthese":
            return TokenLParenthese()
        if string == "RParenthese":
            return TokenRParenthese()

        if string.startswith("Number"):
            data = int(string[len("Number") + 1:-1])
            return Token("Number", data)

        return None


class TokenPlus(Token):  # pylint: disable=R0903
    """Operator '+' token"""
    def __init__(self,
                 line: int | None = None,
                 column: int | None = None):
        super().__init__("Plus", None, line, column)


class TokenMinus(Token):  # pylint: disable=R0903
    """Operator '-' token"""
    def __init__(self,
                 line: int | None = None,
                 column: int | None = None):
        super().__init__("Minus", None, line, column)


class TokenMultiply(Token):  # pylint: disable=R0903
    """Operator '*' token"""
    def __init__(self,
                 line: int | None = None,
                 column: int | None = None):
        super().__init__("Multiply", None, line, column)


class TokenDivision(Token):  # pylint: disable=R0903
    """Operator '/' token"""
    def __init__(self,
                 line: int | None = None,
                 column: int | None = None):
        super().__init__("Division", None, line, column)


class TokenLParenthese(Token):  # pylint: disable=R0903
    """'(' token"""
    def __init__(self,
                 line: int | None = None,
                 column: int | None = None):
        super().__init__("LParenthese", None, line, column)


class TokenRParenthese(Token):  # pylint: disable=R0903
    """')' token"""
    def __init__(self,
                 line: int | None = None,
                 column: int | None = None):
        super().__init__("RParenthese", None, line, column)


if __name__ == "__main__":
    token1 = Token("Plus")
    token2 = Token("Plus")
    print(token1 == token2)
