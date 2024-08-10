class Interpreter:

    def interpret(self, expr):
        if expr == "true" or expr=="false" or expr=="nil" or isinstance(expr, str):
            return expr
        elif isinstance(expr, str):
            try:
                retVal = float(expr)
                if retVal.is_integer():
                    retVal = int(retVal)
                return retVal
            except ValueError:
                return expr
        elif isinstance(expr, (int, float)):
            retVal = expr
            if isinstance(retVal, float) and retVal.is_integer():
                retVal = int(retVal)
            return retVal