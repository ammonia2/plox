from app.visitor import Visitor, Binary, Grouping, Literal, Unary

class Interpreter:

    def interpret(self, expr):
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Grouping):
            return self.interpret(expr.expression)
        elif isinstance(expr, Unary):
            if expr.operator == "-":
                return -self.interpret(expr.right)
            elif expr.operator == "!":
                if expr.right.value =="false" or expr.right.value == "nil":
                    return "true"
                else: return "false"