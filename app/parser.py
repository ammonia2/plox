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
        else:
            return "error"

    def parse(self):
        print(self.tokenss)
        currToken = self.tokenss[self.curr].tokenType
        print(currToken)
        while(currToken!="EOF"):
            print(self.parse_token(currToken))
            self.curr +=1
            currToken = self.tokenss[self.curr].tokenType

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