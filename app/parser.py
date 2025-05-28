import sys
from app.tokeniser import Token
from app.expression import Binary, Grouping, Literal, Unary
from app.stmt import Block, Class, Expression, Function, If, Print, Return, Var, While

class Parser:
    tokenss: Token = []
    curr: int = 0
    hadError = False
    command: str = ""

    def __init__(self, toka: Token):
        self.tokenss = toka
        
    def parse_token(self, currToken: Token):
        if self.isBool(currToken):
            return Literal(currToken.lexeme)
        elif self.isNil(currToken):
            return Literal(currToken.lexeme)
        elif self.isNum(currToken):
            if self.command != "parse":
                try:
                    if int(currToken.literal)==float(currToken.literal):
                        return Literal(int(currToken.literal))
                    return Literal(float(currToken.literal))
                except ValueError:
                    return Literal(float(currToken.literal))
            else:
                return Literal(currToken.literal)
        elif self.isStr(currToken):
            return Literal(currToken.literal)
        elif self.isBracket(currToken) == 1:
            expr = self.expression()
            if self.curr < len(self.tokenss) and self.tokenss[self.curr].tokenType == "RIGHT_PAREN" and expr != "":
                self.curr += 1
                return Grouping(expr)
            else:
                self.hadError = True
                return None
        
        self.reportError(currToken)

    def expression(self):
        return self.equality()

    def equality(self):
        expr = self.comparison()
        token = self.tokenss[self.curr] if not self.isAtEnd() else None
        while token and (token.tokenType == "BANG_EQUAL" or token.tokenType == "EQUAL_EQUAL"):
            operator = token.lexeme
            self.curr += 1
            right = self.comparison()
            token = self.tokenss[self.curr] if not self.isAtEnd() else None
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self):
        expr = self.term()
        token = self.tokenss[self.curr] if not self.isAtEnd() else None
        while token and (token.tokenType == "GREATER" or token.tokenType == "GREATER_EQUAL" or token.tokenType == "LESS" or token.tokenType == "LESS_EQUAL"):
            operator = token.lexeme
            self.curr += 1
            right = self.term()
            token = self.tokenss[self.curr] if not self.isAtEnd() else None
            expr = Binary(expr, operator, right)
        return expr

    def term(self):
        expr = self.factor()
        token = self.tokenss[self.curr] if not self.isAtEnd() else None
        while token and (token.tokenType == "MINUS" or token.tokenType == "PLUS"):
            operator = token.lexeme
            self.curr += 1
            right = self.factor()
            token = self.tokenss[self.curr] if not self.isAtEnd() else None
            expr = Binary(expr, operator, right)
        return expr

    def factor(self):
        expr = self.unary()
        token = self.tokenss[self.curr] if not self.isAtEnd() else None
        while token and (token.tokenType == "STAR" or token.tokenType == "SLASH"):
            operator = token.lexeme
            self.curr += 1
            right = self.unary()
            token = self.tokenss[self.curr] if not self.isAtEnd() else None
            expr = Binary(expr, operator, right)
        return expr

    def unary(self):
        token = self.tokenss[self.curr]
        if token.tokenType == "BANG" or token.tokenType == "MINUS":
            operator = token.lexeme
            self.curr += 1
            right = self.unary()
            return Unary(operator, right)

        self.curr += 1 if not self.isAtEnd() else 0
        return self.parse_token(token)

    def parse(self, cmd):
        self.command = cmd
        
        if cmd == "run":
            statements = []
            while not self.isAtEnd():
                stmt = self.statement()
                statements.append(stmt)
            if not self.hadError:
                return statements
        else:
            expr = self.expression()
            if not self.hadError:
                return expr        
        return None
    
    # Expanded Grammar
    # program        → statement* EOF ;
    # statement      → exprStmt | printStmt ;
    # exprStmt       → expression ";" ;
    # printStmt      → "print" expression ";" ;
    def statement(self):
        if self.isAtEnd():
            return None
        
        token = self.tokenss[self.curr]
        if token.tokenType == "PRINT":
            self.curr += 1
            return self.printStatement()
        
        return self.expressionStatement()
    
    def printStatement(self):
        # no expr and no semicolon
        if self.isAtEnd():
            self.hadError = True
            printToken = self.tokenss[self.curr - 1]
            print(f"[line {printToken.lineNum}] Error at 'print': Expect expression after 'print'.", file=sys.stderr)
            return None

        # no expr after print
        if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "SEMICOLON":
            self.hadError = True
            print(f"[line {self.tokenss[self.curr].lineNum}] Error at '{self.tokenss[self.curr].lexeme}': Expect Expression.", file=sys.stderr)
            self.curr += 1
            return None
    
        expr = self.expression()
        if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "SEMICOLON":
            self.curr += 1
        else:
            # Missing semicolon is still an error
            self.hadError = True
            print(f"[line {self.tokenss[self.curr-1].lineNum}] Error: Expect ';' after print statement.", file=sys.stderr)
        
        return Print(expr)
    
    def expressionStatement(self):
        expr = self.expression()

        if self.isAtEnd():
            self.hadError = True
            print(f"[line {self.tokenss[self.curr-1].lineNum}] Error: Expect ';' after expression.", file=sys.stderr)
            return Expression(expr)
        
        if self.tokenss[self.curr].tokenType == "SEMICOLON":
            self.curr += 1
        else:
            # Error: missing semicolon
            token = self.tokenss[self.curr - 1]
            self.hadError = True
            print(f"[line {token.lineNum}] Error: Expect ';' after expression.", file=sys.stderr)
        
        return Expression(expr) if not self.hadError else None

    def isBracket(self, token) -> int:
        if token.tokenType == "LEFT_PAREN": return 1
        elif token.tokenType == "RIGHT_PAREN": return 2
        else: return 0

    def isBool(self, token) -> bool:
        return token.tokenType == "TRUE" or token.tokenType == "FALSE"

    def isNil(self, token) -> bool:
        return token.tokenType == "NIL"
    
    def isNum(self, token) -> bool:
        return token.tokenType == "NUMBER"

    def isStr(self, token) -> bool:
        return token.tokenType == "STRING"

    def isAtEnd(self) -> bool:
        return self.curr >= len(self.tokenss) or (self.curr < len(self.tokenss) and self.tokenss[self.curr].tokenType == "EOF")

    def reportError(self, token):
        self.hadError = True
        print(f"[line {token.lineNum}] Error at '{token.lexeme}': Expect Expression.", file=sys.stderr)