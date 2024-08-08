from abc import ABC, abstractmethod
from expressions import Binary, Grouping, Literal, Unary

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