class Interpreter:

    def interpret(self, expr):
        if expr == "true" or expr=="false" or expr=="nil" or isinstance(expr, str):
            return expr
        elif isinstance(expr, str):
            try:
                return int(expr)
            except ValueError:
                try:
                    return float(expr)
                except ValueError:
                    return expr