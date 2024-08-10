class Interpreter:

    def interpret(self, expr):
        if expr == "true" or expr=="false" or expr=="nil" or isinstance(expr, str):
            return expr
        elif isinstance(expr, str):
            if '.' in expr:
                return float(expr)
            else:
                return int(expr)