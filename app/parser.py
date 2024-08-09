from app.tokeniser import Token

class Parser:
    tokenss: Token = []
    curr: int = 0
    start: int = 0
    outStr: str = ""
    openingB: int=0
    closingB: int=0
    hadError = False

    def __init__(self, toka: Token):
        self.tokenss = toka
        
    def parse_token(self, currToken):
        if self.isBool(currToken):
            self.outStr+= currToken.lexeme
        elif self.isNil(currToken):
            self.outStr+= currToken.lexeme
        elif self.isNum(currToken):
            self.outStr+= currToken.literal
        elif self.isStr(currToken):
            self.outStr+= currToken.literal
        elif self.isBracket(currToken)>0:
            if (self.isBracket(currToken)==1):
                self.openingB+=1
                self.outStr+= currToken.lexeme + "group "
                if (self.tokenss[self.curr+1] and self.isBracket(self.tokenss[self.curr])):
                    self.hadError = True
            elif (self.isBracket(currToken)==2):
                self.closingB += 1
                self.outStr+= currToken.lexeme

    def parse(self):
        while not self.isAtEnd() and self.tokenss[self.curr].tokenType != "EOF":
            currToken = self.tokenss[self.curr]
            self.parse_token(currToken)
            if (self.openingB == self.closingB):
                print(self.outStr)
                self.outStr = ""
            self.curr += 1

        if (self.openingB != self.closingB):
            self.hadError = True

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
