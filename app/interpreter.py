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
                value = self.interpret(expr.right)
                if value =="false" or value == "nil":
                    return "true"
                else: return "false"
        elif isinstance(expr, Binary):
            left = self.interpret(expr.left)
            right = self.interpret(expr.right)
            if expr.operator=='-':
                return left - right
            elif expr.operator == '*':
                return left * right
            elif expr.operator == '/':
                try:
                    int(left)
                    int(right)
                    if (left%right == 0):
                        return left // right
                    return left / right
                except ValueError:
                    return left / right
            elif expr.operator == '+':
                if (isinstance(left, int) and isinstance(right, int)) or (isinstance(left, float) and isinstance(right, float)):
                    return left + right
                else:
                    return str(left) + str(right)
            elif expr.operator == '>':
                return "true" if left > right else "false"
            elif expr.operator == '<':
                return "true" if left < right else "false"
            elif expr.operator == '>=':
                return "true" if left >= right else "false"
            elif expr.operator == '<=':
                return "true" if left <= right else "false"
            elif expr.operator == '==':
                return "true" if left == right else "false"
            elif expr.operator == '!=':
                return "true" if left != right else "false"