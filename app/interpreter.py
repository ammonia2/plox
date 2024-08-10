class Interpreter:

    def interpret(self, expr):
        if expr == "true" or expr=="false" or expr=="nil" or isinstance(expr, str):
            return expr
        elif isinstance(expr, str):
            if expr.isdigit() or (expr[0] == '-' and expr[1:].isdigit()):
                return int(expr)
            try:
                return float(expr)
            except ValueError:
                return expr