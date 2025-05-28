from abc import ABC, abstractmethod
from app.tokeniser import Token

class Block:
    def __init__(self, stmts):
        self.stmts = stmts

    def accept(self, visitor):
        return visitor.visitBlock(self)
    
class Class:
    def __init__(self, name: Token, superclass: Token, methods):
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor):
        return visitor.visitClass(self)
    
class Expression:
    def __init__(self, expr):
        self.expression = expr

    def accept(self, visitor):
        return visitor.visitExpression(self)
    
class Function:
    def __init__(self, name: Token, params, body):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visitFunction(self)
    
class If:
    def __init__(self, condition, thenBranch, elseBranch):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def accept(self, visitor):
        return visitor.visitIf(self)

class Print:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitPrint(self)
    
class Return:
    def __init__(self, keyword: Token, value):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visitReturn(self)
    
class Var:
    def __init__(self, name:Token, initializer):
        self.name = name
        self.initialiser = initializer

    def accept(self, visitor):
        return visitor.visitVar(self)
    
class While:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def accept(self, visior):
        return visior.visitWhile(self)
    

class StmtVisitor(ABC):
    @abstractmethod
    def visitWhile(self, expr):
        pass

    @abstractmethod
    def visitBlock(self, stmt):
        pass

    @abstractmethod
    def visitClass(self, stmt):
        pass

    @abstractmethod
    def visitExpression(self, expr):
        pass

    @abstractmethod
    def visitFunction(self, stmt):
        pass

    @abstractmethod
    def visitIf(self, stmt):
        pass

    @abstractmethod
    def visitPrint(self, stmt):
        pass

    @abstractmethod
    def visitReturn(self, stmt):
        pass

    @abstractmethod
    def visitVar(self, stmt):
        pass

class PrintStmtVisitor(StmtVisitor):
    def visitWhile(self, expr):
        pass

    def visitBlock(self, stmt):
        pass

    def visitClass(self, stmt):
        pass

    def visitExpression(self, expr):
        return f'(expression {expr.expression.accept(self)})'

    def visitFunction(self, stmt):
        pass

    def visitIf(self, stmt):
        pass

    def visitPrint(self, stmt):
        return f'(print {stmt.expression.accept(self)})'

    def visitReturn(self, stmt):
        pass

    def visitVar(self, stmt):
        if stmt.initialiser is None:
            return f"(var {stmt.name.lexeme})"
        return f"(var {stmt.name.lexeme} {stmt.initialiser.accept(self)})"