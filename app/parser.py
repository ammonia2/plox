from app.tokeniser import Token

class Parser:
    tokenss: Token = []
    curr: int = 0
    start: int = 0

    def __init__(self, toka: Token):
        self.tokenss = toka
        
    def parse_token(self, currToken):
        if self.isBool(currToken):
            print(currToken.lexeme)
            return currToken.lexeme
        elif self.isNil(currToken):
            return currToken.lexeme
        # else:
        #     return "error"

    def parse(self):
        currToken = self.tokenss[self.curr]
        while(currToken.tokenType!="EOF"):
            print(self.parse_token(currToken))
            self.curr +=1 if not self.isAtEnd() else 0
            currToken = self.tokenss[self.curr]

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

    def isBool(self, token):
        return (token.tokenType=="TRUE" or token.tokenType == "FALSE")

    def isNil(self, token):
        return token.tokenType=="nil"

    def isAtEnd(self):
        return self.curr < len(self.tokenss)