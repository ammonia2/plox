from abc import ABC, abstractmethod

class Binary:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinary(self)

class Grouping:
    def __init__(self, expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitGrouping(self)

class Literal:
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteral(self)

class Unary:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnary(self)

class Visitor(ABC):
    @abstractmethod
    def visitBinary(self, expr: Binary):
        pass

    @abstractmethod
    def visitGrouping(self, expr: Grouping):
        pass

    @abstractmethod
    def visitLiteral(self, expr: Literal):
        pass

    @abstractmethod
    def visitUnary(self, expr: Unary):
        pass

class PrintVisitor(Visitor):
    def visitBinary(self, expr: Binary):
        return f"({expr.operator.lexeme} {expr.left.accept(self)} {expr.right.accept(self)})"

    def visitGrouping(self, expr: Grouping):
        return self.parenthesize("group", expr.expression)

    def visitLiteral(self, expr: Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visitUnary(self, expr: Unary):
        return f"({expr.operator.lexeme} {expr.right.accept(self)})"

    def parenthesize(self, name, *exprs):
        string = f"({name}"
        for expr in exprs:
            string += f" {expr.accept(self)}"
        string += ")"
        return string