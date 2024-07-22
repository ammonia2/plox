import sys

class Token:
    tokenType:str
    lexeme: str # the field name of token in tokenDict
    literal: str
    lineNum: int

    def __init__(self, t:str, lex:str, lit:str, ln:int):
        self.tokenType = t
        self.lexeme = lex
        self.literal = lit
        self.lineNum = ln

    def tokenisedForm(self) -> str:
        return (self.tokenType + " " + self.lexeme + " " + self.literal)

class Scanner:
    source :str # raw source code string
    tokenss: Token = []
    lineNum: int = 1
    start: int = 0
    current: int =0
    hadError = False

    def __init__(self, content:str):
        self.source = content

    def addToken(self, token:Token):
        self.tokenss.append(token)

    def createTokens(self):
        while (self.isAtEnd() != True):
            self.start = self.current
            self.scanToken()

        self.tokenss.append(Token("EOF", "", "null", self.lineNum))
        print("EOF  null")

    def scanToken(self):
        char = self.source[self.start]
        next_char = self.source[self.start+1] if (self.start+1 < len(self.source)) else ''
        char_combo = char +next_char
        if (char_combo == '//'):
            self.eoline()
        elif (char == '"'):
            strVal = "\""
            self.current+=1
            while (self.isAtEnd()!=True and self.source[self.current] != '"'):
                stringVal += self.source[self.current]
                if (self.source[self.current] == '\n'): self.lineNum +=1
                self.current+=1
            stringVal += '\"'
            if (self.isAtEnd()):
                self.reportError(self.lineNum, "Unterminated string.")
                return

            newToken = Token("STRING", stringVal, stringVal[1:-1], self.lineNum)
            self.addToken(newToken)
            print(newToken.tokenisedForm())         

        elif (char_combo in tokenDict):
            newToken = Token(tokenDict[char_combo], char_combo, "null", self.lineNum)
            print(newToken.tokenisedForm())
            self.addToken(newToken)
            self.current+=2
        elif char in tokenDict:
            newToken = Token(tokenDict[char], char, "null", self.lineNum)
            print(newToken.tokenisedForm())
            self.addToken(newToken)
            self.current+=1
        elif char==' ' or char == '\n' or char == '\t':
            self.current+=1
            if (char == '\n'): self.lineNum+=1
        else:
            self.reportError(self.lineNum,"Unexpected character", char)
            self.current+=1

    def eoline(self):
        while (self.isAtEnd()!=True and self.source[self.current] != '\n'):
            self.current+=1

    def isAtEnd(self) -> bool:
        return (self.current >= len(self.source))

    def reportError(self, lineNum, errType, char=''):
        self.hadError = True
        if errType=="Unexpected character":
            print(f"[line {lineNum}] Error: {errType}: {char}", file=sys.stderr)
        else:
            print(f"[line {lineNum}] Error: {errType}", file=sys.stderr)

tokenDict = {
    '(': "LEFT_PAREN",
    ')': "RIGHT_PAREN",
    '{': "LEFT_BRACE",
    '}': "RIGHT_BRACE",
    '*': "STAR",
    '.': "DOT",
    ',': "COMMA",
    '+': "PLUS",
    '-': "MINUS",
    ';': "SEMICOLON",
    '=': "EQUAL",
    '==': "EQUAL_EQUAL",
    '!': "BANG",
    '!=': "BANG_EQUAL",
    '<': "LESS",
    '<=': "LESS_EQUAL",
    '>': "GREATER",
    '>=': "GREATER_EQUAL",
    '/': "SLASH",
}

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    scanner = Scanner(file_contents)
    if file_contents:
        scanner.createTokens()
    else:
        scanner.addToken(Token("EOF", "", "null", 1))
        print("EOF  null") # Placeholder, remove this line when implementing the scanner

    if (scanner.hadError):
        exit(65)

if __name__ == "__main__":
    main()
