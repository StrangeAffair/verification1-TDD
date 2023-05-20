class Token:
    def __init__(self, type: str, data: int | None=None, line=None, column=None):
        self.type   = type
        self.data   = data
        self.line   = line
        self.column = column
    
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        if self.data is not None:
            return f"{self.type}({self.data})"
        else:
            return f"{self.type}"
    
    def __eq__(self, other):
        if type(other) == str:
            return self.type == other
        
        if isinstance(other, Token):
            return (self.type == other.type) and (self.data == other.data)

class TokenPlus(Token):
    def __init__(self, line: int = None, column: int = None) -> None:
        super().__init__("Plus", None, line, column)
class TokenMinus(Token):
    def __init__(self, line: int = None, column: int = None) -> None:
        super().__init__("Minus", None, line, column)

class TokenLParenthese(Token):
    def __init__(self, line: int = None, column: int = None) -> None:
        super().__init__("LParenthese", None, line, column)
class TokenRParenthese(Token):
    def __init__(self, line: int = None, column: int = None) -> None:
        super().__init__("RParenthese", None, line, column)
        
if __name__ == "__main__":
    token1 = Token("Plus")
    token2 = Token("Plus")
    print(token1 == token2)