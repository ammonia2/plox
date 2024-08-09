from app.tokeniser import Token

class Parser:
    tokenss: Token = []
    curr: int = 0
    start: int = 0

    def __init__(self, toka: Token):
        self.tokenss = toka
        
    def parse_token(self, currToken):
        if self.isBool(currToken):
            return currToken.lexeme
        elif self.isNil(currToken):
            return currToken.lexeme
        elif self.isNum(currToken):
            return currToken.lexeme

    def parse(self):
        while not self.isAtEnd() and self.tokenss[self.curr].tokenType != "EOF":
            currToken = self.tokenss[self.curr]
            print(self.parse_token(currToken))
            self.curr += 1

    def equality(self):
        pass

    def match(self):
        pass

    def check(self):
        pass

    def binary(self):
        pass

    def grouping(self):
        pass

    def literal(self):
        pass

    def unary(self):
        pass

    def isBool(self, token) -> bool:
        return (token.tokenType=="TRUE" or token.tokenType == "FALSE")

    def isNil(self, token) -> bool:
        return token.tokenType=="NIL"

    def isFloat(self, token_literal: str) -> bool:
        try:
            float(token_literal)
            return True
        except ValueError:
            return False
    
    def isNum(self, token) -> bool:
        return self.isFloat(token.literal)

    def isAtEnd(self) -> bool:
        return self.curr >= len(self.tokenss)
