import sys
from app.tokeniser import Token

def Binary(left, operator, right):
    return {"left": left, "operator": operator, "right": right}

def Grouping(expression):
    return f"(group {expression})"

def Literal(val):
    if val is None:
        return "nil"
    return str(val).lower()
    
def Unary(operator, right):
    return f"({operator} {right})"

class Parser:
    tokenss: Token = []
    curr: int = 0
    # openingB: int=0
    # closingB: int=0
    hadError = False

    def __init__(self, toka: Token):
        self.tokenss = toka
        
    def parse_token(self, currToken):
        if self.isBool(currToken):
            return currToken.lexeme
        elif self.isNil(currToken):
            return currToken.lexeme
        elif self.isNum(currToken):
            return currToken.literal
        elif self.isStr(currToken):
            return currToken.literal
        elif self.isBracket(currToken)==1:
            # self.curr +=1
            expr = self.expression()
            if self.curr < len(self.tokenss) and self.tokenss[self.curr].tokenType == "RIGHT_PAREN" and expr!="":
                self.curr += 1
            else: self.hadError= True
            return Grouping(expr)
        
    def expression(self):
        return self.equality() 

    def equality(self):
        return self.comparison() 

    def comparison(self):
        return self.term()

    def term(self):
        return self.factor()

    def factor(self):
        return self.unary()

    def binary(self):
        pass

    def literal(self):
        pass

    def unary(self):
        token = self.tokenss[self.curr]
        if token.tokenType == "BANG" or token.tokenType == "MINUS":
            operator = token.lexeme
            self.curr +=1
            right = self.unary()
            return Unary(operator, right)

        self.curr +=1 if (not self.isAtEnd()) else 0
        return self.parse_token(token)

    def parse(self):
        expr = self.expression()
        if not self.hadError:
            print(expr)

    def isBracket(self, token) -> int:
        if token.tokenType=="LEFT_PAREN": return 1
        elif token.tokenType == "RIGHT_PAREN": return 2
        else: return 0

    def isBool(self, token) -> bool:
        return (token.tokenType=="TRUE" or token.tokenType == "FALSE")

    def isNil(self, token) -> bool:
        return token.tokenType=="NIL"
    
    def isNum(self, token) -> bool:
        return token.tokenType == "NUMBER"

    def isStr(self, token) -> bool:
        return token.tokenType == "STRING"

    def isAtEnd(self) -> bool:
        return self.curr >= len(self.tokenss)
