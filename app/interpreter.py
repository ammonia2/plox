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
                result = not self.interpret(expr.right)
                if result == False:
                    return "false"
                elif result == True:
                    return "true"
                return result