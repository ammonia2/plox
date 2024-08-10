import sys
from app.visitor import Visitor, Binary, Grouping, Literal, Unary

class Interpreter:
    hadError = False

    def interpret(self, expr):
        if isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Grouping):
            return self.interpret(expr.expression)
        elif isinstance(expr, Unary):
            if expr.operator == "-":
                right = self.interpret(expr.right)
                if isinstance(right, int) or isinstance(right, float):
                    return -right
                else:
                    self.reportError("unary")
            elif expr.operator == "!":
                value = self.interpret(expr.right)
                if value =="false" or value == "nil":
                    return "true"
                else: return "false"
        elif isinstance(expr, Binary):
            left = self.interpret(expr.left)
            right = self.interpret(expr.right)
            if expr.operator=='-':
                if (not isinstance(left, int) and not isinstance(left, float) )or (not isinstance(right, int) and not isinstance(right, float)):
                    self.reportError("binary")
                return left - right
            elif expr.operator == '*':
                if (not isinstance(left, int) and not isinstance(left, float) )or (not isinstance(right, int) and not isinstance(right, float)):
                    self.reportError("binary")
                return left * right
            elif expr.operator == '/':
                if (not isinstance(left, int) and not isinstance(left, float) )or (not isinstance(right, int) and not isinstance(right, float)):
                    self.reportError("binary")
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
                elif (isinstance(left, str) and isinstance(right, str)):
                    return str(left) + str(right)
                else:
                    self.reportError("string")
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

    def reportError(self, type):
        self.hadError = True
        if type == "unary":
            print("Operand must be a number.", file=sys.stderr)
        elif type == "binary":
            print("Operands must be numbers.", file=sys.stderr)
        elif type == "string":
            print("Operands must be two numbers or two strings.", file=sys.stderr)
        exit(70)