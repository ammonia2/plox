class Interpreter:

    def interpret(self, expr):
        if expr == "true" or expr=="false" or expr=="nil":
            return expr