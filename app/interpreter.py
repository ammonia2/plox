from app.visitor import Visitor, Binary, Grouping, Literal, Unary

class Interpreter:

    def interpret(self, expr):
        if isinstance(expr, Literal):
            return expr.value