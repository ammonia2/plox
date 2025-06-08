import sys
from app.tokeniser import Token
from app.parser import Parser
from app.scanner import Scanner
from app.expression import ExpressionVisitor, PrintExpressionVisitor
from app.statement import StmtVisitor, PrintStmtVisitor
from app.interpreter import Interpreter

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh \"command\" <filename>", file=sys.stderr)
        exit(1)

    command: str = sys.argv[1]
    filename: str = sys.argv[2]

    commands = ["parse", "tokenize", "evaluate", "run", "debug"] # debug is for self debugging using PrintVisitors

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
        printer = PrintExpressionVisitor()
        print(expr.accept(printer))
    elif command=="evaluate":
        scanner.createTokens(command)
        parser = Parser(scanner.tokenss)
        expr=parser.parse(command)
        interp = Interpreter()
        print(interp.interpret(expr))
    elif command=="run":
        scanner.createTokens(command)
        parser = Parser(scanner.tokenss)
        statements = parser.parse(command)
        
        if parser.hadError:
            exit(65)

        interp = Interpreter()
        for stmt in statements:
            interp.interpret(stmt)
    elif command == "debug":
        scanner.createTokens(command)
        parser = Parser(scanner.tokenss)
        statements = parser.parse("run")
        
        if parser.hadError:
            exit(65)
        
        # Create printers for both types
        expr_printer = PrintExpressionVisitor()
        stmt_printer = PrintStmtVisitor()

    if (scanner.hadError):
        exit(65)

if __name__ == "__main__":
    main()
