class Interpreter:

    def interpret(self, expr):
        # Handle boolean literals and nil
        if expr == "true" or expr == "false" or expr == "nil":
            return expr

        # Try to convert to an integer
        try:
            return int(expr)
        except ValueError:
            pass  # If it fails, proceed to the next check

        # Try to convert to a float
        try:
            return float(expr)
        except ValueError:
            pass  # If it fails, return the expression as-is

        # If it's neither an int nor a float, return it as is
        return expr
