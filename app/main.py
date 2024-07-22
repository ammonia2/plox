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

    def addToken(self, token:Token):
        self.tokenss.append(token)

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
}

primaryScanner = Scanner()

hadError = False

def reportError(lineNum, char):
    global hadError
    hadError = True
    print(f"[line {lineNum}] Error: Unexpected character: {char}", file=sys.stderr)

def createTokens(filename: str):
    global primaryScanner, tokenDict
    lineNum = 1
    with open(filename) as file:
        for line in file:
            words = line.split()
            wordLen = len(words)
            for i, word in enumerate(words):
                j = 0
                while j < len(word):
                    char = word[j]
                    next_char = word[j + 1] if j + 1 < len(word) else ''
                    char_combo = char + next_char
            
                    if char_combo in tokenDict:
                        newToken = Token(tokenDict[char_combo], char_combo, "null", lineNum)
                        print(newToken.tokenisedForm())
                        primaryScanner.addToken(newToken)
                        j +=2
                    elif char in tokenDict:
                        newToken = Token(tokenDict[char], char, "null", lineNum)
                        print(newToken.tokenisedForm())
                        primaryScanner.addToken(newToken)
                        j+=1
                    else:
                        reportError(lineNum, char)
                        j +=1
            
            lineNum += 1
    
    print("EOF  null")

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
        createTokens(filename)
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner

    if (hadError):
        exit(65)

if __name__ == "__main__":
    main()
