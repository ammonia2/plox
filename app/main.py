import sys

def createTokens(fileContents: str):
    words = fileContents.split()
    i=0
    wordLen = len(words)
    for word in words:
        for char in word:
            if char == '(':
                print("LEFT_PAREN ( null")
            elif (char == ')'):
                print("RIGHT_PAREN ( null")
        i+=1
        if (i<wordLen):
            print("IDENTIFIER space null")

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
        createTokens(file_contents)
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner


if __name__ == "__main__":
    main()
