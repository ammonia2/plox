import sys
from app.tokeniser import Token
from app.parser import Parser
from app.scanner import Scanner
from app.visitor import Visitor, PrintVisitor
from app.interpreter import Interpreter

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh \"command\" <filename>", file=sys.stderr)
        exit(1)

    command: str = sys.argv[1]
    filename: str = sys.argv[2]

    commands = ["parse", "tokenize", "evaluate"]

    if command not in commands:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()

    scanner = Scanner(file_contents)
    if command == "tokenize":
        if file_contents:
            scanner.createTokens(command)
        else:
            scanner.addToken(Token("EOF", "", "null", 1))
            print("EOF  null") # Placeholder, remove this line when implementing the scanner
    elif command== "parse":
        scanner.createTokens(command)
        parser = Parser(scanner.tokenss)
        expr=parser.parse(command)
        if parser.hadError: 
            exit(65)
        printer = PrintVisitor()
        print(expr.accept(printer))
    elif command=="evaluate":
        scanner.createTokens(command)
        parser = Parser(scanner.tokenss)
        expr=parser.parse(command)
        interp = Interpreter()
        print(interp.interpret(expr))

    if (scanner.hadError):
        exit(65)

if __name__ == "__main__":
    main()
