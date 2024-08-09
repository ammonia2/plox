import sys
from app.tokeniser import Token

def Binary(left, operator, right):
    return f"({operator} {left} {right})"

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
            expr = self.expression()
            if self.curr < len(self.tokenss) and self.tokenss[self.curr].tokenType == "RIGHT_PAREN" and expr!="":
                self.curr += 1
                return Grouping(expr)
            else: 
                self.hadError= True
                return None
        
        return None
        
    def expression(self):
        return self.equality()

    def equality(self):
        expr= self.comparison()
        token = self.tokenss[self.curr]
        while token.tokenType=="BANG_EQUAL" or token.tokenType=="EQUAL_EQUAL":
            operator = token.lexeme
            self.curr+=1
            right = self.comparison()
            token = self.tokenss[self.curr] if not self.isAtEnd() else None
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr= self.term()
        token = self.tokenss[self.curr]
        while token.tokenType=="GREATER" or token.tokenType=="GREATER_EQUAL" or token.tokenType =="LESS" or token.tokenType=="LESS_EQUAL":
            operator = token.lexeme
            self.curr+=1
            right = self.term()
            token = self.tokenss[self.curr] if not self.isAtEnd() else None
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr= self.factor()
        token = self.tokenss[self.curr]
        while token.tokenType=="MINUS" or token.tokenType =="PLUS":
            operator = token.lexeme
            self.curr+=1
            right = self.unary()
            token = self.tokenss[self.curr] if not self.isAtEnd() else None
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        expr= self.unary()
        token = self.tokenss[self.curr]
        while token.tokenType=="STAR" or token.tokenType =="SLASH":
            operator = token.lexeme
            self.curr+=1
            right = self.unary()
            token = self.tokenss[self.curr] if not self.isAtEnd() else None
            expr = Binary(expr, operator, right)
        return expr

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
