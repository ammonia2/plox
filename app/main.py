import sys

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
}

hadError = False

def reportError(lineNum, char):
    hadError = True
    print(f"[line {lineNum}] Error: Unexpected character: {char}", file=sys.stderr)

def createTokens(filename: str):
    lineNum = 0
    with open(filename) as file:
        i=0
        line = file.readline()
        words = line.split()
        wordLen = len(words)
        for word in words:
            for char in word:
                if char in tokenDict:
                    print(f"{tokenDict[char]} {char} null")
                else:
                    reportError(lineNum, char)
            i+=1
            if (i<wordLen):
                print("IDENTIFIER space null")
        
        lineNum+=1
    
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
        sys.exit(65)

if __name__ == "__main__":
    main()
