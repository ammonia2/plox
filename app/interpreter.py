class Interpreter:

    def interpret(self, expr):
        if expr == "true" or expr=="false" or expr=="nil" or isinstance(expr, str):
            return expr
        elif expr.isdigit():
            return int(expr)
        elif a.replace('.','',1).isdigit() and a.count('.') < 2:
            return float(expr)