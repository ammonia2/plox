from app.visitor import Visitor, Binary, Grouping, Literal, Unary

class Interpreter:

    def interpret(self, expr):
        if isinstance(expr, Literal):
            return expr.value
        elif int(expr):
            return int(expr)
        elif float(expr):
            return float(expr)
        else:
            return expr