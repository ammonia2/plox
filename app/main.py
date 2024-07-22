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

    def __init__(self, content:str):
        self.source = content

    def addToken(self, token:Token):
        self.tokenss.append(token)

    def createTokens(self):
        while (self.isAtEnd() != True):
            self.start = self.current
            self.scanToken()

        tokenss.append(Token("EOF", "", null, lineNum))
        print("EOF  null")

    def scanToken(self):
        char = source[self.start]
        next_char = source[self.start+1] if (self.start+1 <= len(source)) else ''
        char_combo = char +next_char
        if (char_combo in tokenDict):
            newToken = Token(tokenDict[char_combo], char_combo, "null", lineNum)
            print(newToken.tokenisedForm())
            self.addToken(newToken)
            self.current+=2
        elif char in tokenDict:
            newToken = Token(tokenDict[char], char, "null", lineNum)
            print(newToken.tokenisedForm())
            self.addToken(newToken)
            self.current+=1
        else:
            reportError(lineNum, char)
            j +=1

    def isAtEnd(self) -> bool:
        return (self.current >= source.length())

tokenDict = {
    '(': "LEFT_PAREN",
    ')': "RIGHT_PAREN",
    '{': "LEFT_BRACE",
    '}': "RIGHT_BRACE",
    '*': "STAR",
    '.': "DOT",
    ',': "COMMA",
    '+': "PLUS",
    '/': "SLASH",
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
}

hadError = False

def reportError(lineNum, char):
    global hadError
    hadError = True
    print(f"[line {lineNum}] Error: Unexpected character: {char}", file=sys.stderr)

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

    # Uncomment this block to pass the first stage
    if file_contents:
        scanner = Scanner(file_contents)
        scanner.createTokens()
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner

    if (hadError):
        exit(65)

if __name__ == "__main__":
    main()
