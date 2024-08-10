class Interpreter:

    def interpret(self, expr):
        if expr == "true" or expr=="false" or expr=="nil":
            return expr
        elif int(expr):
            return int(expr)
        elif float(expr):
            return float(expr)
        else:
            return expr