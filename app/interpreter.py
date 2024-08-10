from app.visitor import Visitor, Binary, Grouping, Literal, Unary

class Interpreter:

    def interpret(self, expr):
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Grouping):
            return self.interpret(expr.expression)
        