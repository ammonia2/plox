import sys
from app.tokeniser import Token
from app.expression import Binary, Grouping, Literal, Unary, Variable, Assign, Logical, Call
from app.statement import Block, Class, Expression, Function, If, Print, Return, Var, While

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
        elif self.isIdentifier(currToken):
            return Variable(currToken)
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
        return self.assignment()
    
    def finishCall(self, callee): # helper to parse arg list
        arguments = []
        if not self.isAtEnd() and self.tokenss[self.curr].tokenType != "RIGHT_PAREN":
            while True:
                if len(arguments) >= 255:
                    self.reportError(self.tokenss[self.curr+1], "Can't have more than 255 arguments.")
                arguments.append(self.expression())
                if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "COMMA":
                    self.curr += 1
                else:
                    break

        if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "RIGHT_PAREN":
            paren: Token = self.tokenss[self.curr]
            self.curr += 1
        else:
            self.reportError(self.tokenss[self.curr - 1], errorText="Expect ')' after arguments.")
            return None

        return Call(callee, paren, arguments)
    
    def call(self): # func call expr parsing
        expr = self.parse_token(self.tokenss[self.curr])

        while True:
            if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "LEFT_PAREN":
                expr = self.finishCall(expr)
            else:
                break

        return expr

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
        return self.call()
    
    def varDeclaration(self):
        if self.isAtEnd() or self.tokenss[self.curr].tokenType != "IDENTIFIER":
            token = self.tokenss[self.curr - 1]
            self.reportError(self.tokenss[self.curr - 1], errorText="Expect variable name.")
            return None

        name = self.tokenss[self.curr]
        self.curr += 1
        initialiser = None
        if (self.tokenss[self.curr].tokenType == "EQUAL"):
            self.curr += 1
            initialiser = self.expression()

        if self.isAtEnd() or self.tokenss[self.curr].tokenType != "SEMICOLON":
            token = self.tokenss[self.curr - 1]
            self.reportError(token, errorText = "Expect ';' after expression.")
        else:
            self.curr += 1
        
        return Var(name, initialiser)
    
    def function(self, kind: str):
        # function name
        if self.isAtEnd() or self.tokenss[self.curr].tokenType != "IDENTIFIER":
            self.reportError(self.tokenss[self.curr - 1], errorText=f"Expect {kind} name.")
            return None
        name = self.tokenss[self.curr]
        self.curr += 1

        # parameter list
        if self.isAtEnd() or self.tokenss[self.curr].tokenType != "LEFT_PAREN":
            self.reportError(self.tokenss[self.curr - 1], errorText=f"Expect '(' after {kind} name.")
            return None
        self.curr += 1

        parameters = []
        if not self.isAtEnd() and self.tokenss[self.curr].tokenType != "RIGHT_PAREN":
            while True:
                if len(parameters) >= 255:
                    self.reportError(self.tokenss[self.curr], errorText="Can't have more than 255 parameters.")
                if self.tokenss[self.curr].tokenType != "IDENTIFIER":
                    self.reportError(self.tokenss[self.curr], errorText="Expect parameter name.")
                    return None
                parameters.append(self.tokenss[self.curr])
                self.curr += 1
                if self.isAtEnd() or self.tokenss[self.curr].tokenType != "COMMA":
                    break
                self.curr += 1
        if self.isAtEnd() or self.tokenss[self.curr].tokenType != "RIGHT_PAREN":
            self.reportError(self.tokenss[self.curr - 1], errorText="Expect ')' after parameters.")
            return None
        self.curr += 1

        # function body
        if self.isAtEnd() or self.tokenss[self.curr].tokenType != "LEFT_BRACE":
            self.reportError(self.tokenss[self.curr - 1], errorText=f"Expect '{{' before {kind} body.")
            return None
        self.curr += 1
        body = self.blockStatement()
        
        if self.isAtEnd() or self.tokenss[self.curr].tokenType != "RIGHT_BRACE":
            self.reportError(self.tokenss[self.curr - 1], errorText=f"Expect '}}' after {kind} body.")
            return None
        self.curr += 1

        return Function(name, parameters, body)

    def declaration(self):
        try:
            if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "FUN":
                self.curr += 1
                return self.function("function")
            elif not self.isAtEnd() and self.tokenss[self.curr].tokenType == "VAR":
                self.curr +=1
                return self.varDeclaration()
            return self.statement()
        except Exception as e:
            # any parsing error
            self.hadError = True
            print(f"Parse error: {e}", file=sys.stderr)
            self.synchronize()
            return None
        
    def OR(self):
        expr = self.AND()
        while not self.isAtEnd() and self.tokenss[self.curr].tokenType == "OR":
            operator: Token = self.tokenss[self.curr]
            self.curr += 1
            right = self.AND()
            expr = Logical(expr, operator, right)

        return expr

    def AND(self):
        expr = self.equality()
        while not self.isAtEnd() and self.tokenss[self.curr].tokenType == "AND":
            operator: Token = self.tokenss[self.curr]
            self.curr += 1
            right = self.equality()
            expr = Logical(expr, operator, right)

        return expr

    def assignment(self):
        expr = self.OR()

        if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "EQUAL":
            equals = self.tokenss[self.curr]
            self.curr += 1
            value = self.assignment()
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            self.reportError(equals, "Invalid assignment target.")
        return expr

    def parse(self, cmd):
        self.command = cmd
        
        if cmd == "run":
            statements = []
            while not self.isAtEnd():
                statements.append(self.declaration())
            if not self.hadError:
                return statements
        else:
            expr = self.expression()
            if not self.hadError:
                return expr        
        return None
    
    def statement(self):
        if self.isAtEnd():
            return None
        
        token: Token = self.tokenss[self.curr]
        if token.tokenType == "FOR":
            self.curr += 1
            return self.forStatement()
        if token.tokenType == "IF":
            self.curr += 1
            return self.ifStatement()
        if token.tokenType == "PRINT":
            self.curr += 1
            return self.printStatement()
        if token.tokenType == "WHILE":
            self.curr += 1
            return self.whileStatement()
        if token.tokenType == "LEFT_BRACE":
            self.curr += 1
            return self.blockStatement()

        return self.expressionStatement()
    
    def forStatement(self):
        if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "LEFT_PAREN":
            self.curr += 1
            initialiser = None
            if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "SEMICOLON":
                self.curr += 1
            elif not self.isAtEnd() and self.tokenss[self.curr].tokenType == "VAR":
                self.curr += 1
                initialiser = self.varDeclaration()
            else:
                initialiser = self.expressionStatement()
    
            # Parse condition
            condition = None
            if not self.isAtEnd() and self.tokenss[self.curr].tokenType != "SEMICOLON":
                condition = self.expression()
            if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "SEMICOLON":
                self.curr += 1
            else:
                self.reportError(self.tokenss[self.curr-1], errorText="Expect ';' after loop condition.")
                return None
    
            # Parse increment
            increment = None
            if not self.isAtEnd() and self.tokenss[self.curr].tokenType != "RIGHT_PAREN":
                increment = self.expression()
            if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "RIGHT_PAREN":
                self.curr += 1
            else:
                self.reportError(self.tokenss[self.curr-1], errorText="Expect ')' after for clauses.")
                return None
    
            body = self.statement()
    
            # Desugaring
            if increment is not None:
                body = Block([body, Expression(increment)])
    
            if condition is None:
                condition = Literal(True)
            body = While(condition, body)
            if initialiser is not None:
                body = Block([initialiser, body])
    
            return body
        else:
            self.reportError(self.tokenss[self.curr-1], errorText="Expect '(' after 'for'.")
            return None

    def ifStatement(self):
        if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "LEFT_PAREN":
            self.curr += 1
            condition = self.expression()
            if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "RIGHT_PAREN":
                self.curr += 1
                thenBranch = self.statement()
                elseBranch = None
                if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "ELSE":
                    self.curr += 1
                    elseBranch = self.statement()
                return If(condition, thenBranch, elseBranch)
            else:
                self.reportError(self.tokenss[self.curr-1], errorText="Expect ')' after if condition.")
                return None
        else:
            self.reportError(self.tokenss[self.curr-1], errorText="Expect '(' after 'if'.")
            return None

    def blockStatement(self):
        stmts: list = []
        while not self.isAtEnd() and not self.tokenss[self.curr].tokenType == "RIGHT_BRACE":
            stmts.append(self.declaration())

        if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "RIGHT_BRACE":
            self.curr += 1
        else:
            self.reportError(self.tokenss[self.curr-1], errorText="Expect '}' after block.")
        return Block(stmts)
    
    def printStatement(self):
        # no expr and no semicolon
        if self.isAtEnd():
            self.hadError = True
            token = self.tokenss[self.curr - 1]
            self.reportError(token, errorText = "Expect ';' after expression.")

            return None
        # no expr after print
        if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "SEMICOLON":
            token = self.tokenss[self.curr - 1]
            self.reportError(token, errorText="Expect Expression.")
            self.curr += 1
            return None
    
        expr = self.expression()
        if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "SEMICOLON":
            self.curr += 1
        else: # missing semicolon
            token = self.tokenss[self.curr - 1]
            self.reportError(token, errorText = "Expect ';' after expression.")

        return Print(expr)
    
    def whileStatement(self):
        if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "LEFT_PAREN":
            self.curr += 1
            condition = self.expression()
            if not self.isAtEnd() and self.tokenss[self.curr].tokenType == "RIGHT_PAREN":
                self.curr += 1
                body = self.statement()
                return While(condition, body)
            else:
                self.reportError(self.tokenss[self.curr-1], errorText="Expect ')' after while condition.")
                return None
        else:
            self.reportError(self.tokenss[self.curr-1], errorText="Expect '(' after 'while'.")
            return None

    def expressionStatement(self):
        expr = self.expression()
        if self.isAtEnd():
            token = self.tokenss[self.curr - 1]
            self.reportError(token, errorText = "Expect ';' after expression.")
            return Expression(expr)
        
        if self.tokenss[self.curr].tokenType == "SEMICOLON":
            self.curr += 1
        else:
            # Error: missing semicolon
            token = self.tokenss[self.curr - 1]
            self.reportError(token, errorText = "Expect ';' after expression.")
        
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
    
    def isIdentifier(self, token) -> bool:
        return token.tokenType == "IDENTIFIER"

    def synchronize(self): # Skip tokens until reaching a statement boundary
        if not self.isAtEnd():
            self.curr += 1
        
        while not self.isAtEnd():
            if self.tokenss[self.curr - 1].tokenType == "SEMICOLON":
                return
            
            currTokenType = self.tokenss[self.curr].tokenType
            if currTokenType in ["CLASS", "FUN", "VAR", "FOR", "IF", 
                                     "WHILE", "PRINT", "RETURN"]:
                return
            
            self.curr += 1

    def reportError(self, token, errorText=None):
        self.hadError = True
        if not errorText:
            print(f"[line {token.lineNum}] Error at '{token.lexeme}': Expect Expression.", file=sys.stderr)
        else:
            print(f"[line {token.lineNum}] Error at '{token.lexeme}': {errorText}", file=sys.stderr)