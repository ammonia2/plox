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
    global hadError
    hadError = True
    print(f"[line {lineNum}] Error: Unexpected character: {char}", file=sys.stderr)

def createTokens(filename: str):
    lineNum = 1
    with open(filename) as file:
        for line in file:  # Process each line in the file
            words = line.split()
            wordLen = len(words)
            for i, word in enumerate(words):
                for char in word:
                    if char in tokenDict:
                        print(f"{tokenDict[char]} {char} null")
                    else:
                        reportError(lineNum, char)
                if i < wordLen - 1:
                    print("IDENTIFIER space null")
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
