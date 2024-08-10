class Interpreter:

    def interpret(self, expr):
        if expr == "true" or expr=="false" or expr=="nil" or isinstance(expr, str):
            return expr
        elif isinstance(expr, int):
            return int(expr)
        elif isinstance(expr, float):
            return float(expr)