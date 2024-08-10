class Token:
    tokenType:str
    lexeme="" # the field name of token in tokenDict
    literal=""
    lineNum: int

    def __init__(self, t:str, lex:str, lit:str, ln:int):
        self.tokenType = t
        self.lexeme = lex
        self.literal = lit
        self.lineNum = ln

    def tokenisedForm(self) -> str:
        return (self.tokenType + " " + str(self.lexeme) + " " + str(self.literal))
