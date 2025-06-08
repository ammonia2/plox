import sys
from app.expression import Binary, Grouping, Literal, Unary, Variable, Assign, Logical
from app.statement import Block, Class, Expression, Function, If, Print, Return, Var, While
from app.environment import Environment

class Interpreter:
    def __init__(self):
        self.hadError = False
        self.environment = Environment()

    def interpret(self, node):
        # -------------- expressions --------------------
        if isinstance(node, Literal):
            return node.value
        elif isinstance(node, Grouping):
            return self.interpret(node.expression)
        elif isinstance(node, Unary):
            if node.operator == "-":
                right = self.interpret(node.right)
                if isinstance(right, int) or isinstance(right, float):
                    return -right
                else:
                    self.reportError("unary")
            elif node.operator == "!":
                value = self.interpret(node.right)
                if value =="false" or value == "nil":
                    return "true"
                else: return "false"
        elif isinstance(node, Binary):
            left = self.interpret(node.left)
            right = self.interpret(node.right)
            if node.operator=='-':
                if (not isinstance(left, int) and not isinstance(left, float) ) or (not isinstance(right, int) and not isinstance(right, float)):
                    self.reportError("binary")
                    return
                return left - right
            elif node.operator == '*':
                if (not isinstance(left, int) and not isinstance(left, float) ) or (not isinstance(right, int) and not isinstance(right, float)):
                    self.reportError("binary")
                return left * right
            elif node.operator == '/':
                if (not isinstance(left, int) and not isinstance(left, float) ) or (not isinstance(right, int) and not isinstance(right, float)):
                    self.reportError("binary")
                try:
                    int(left)
                    int(right)
                    if (left%right == 0):
                        return left // right
                    return left / right
                except ValueError:
                    return left / right
            elif node.operator == '+':
                if (isinstance(left, (int, float)) and isinstance(right, (int, float))):
                    return left + right
                elif (isinstance(left, str) and isinstance(right, str)) and left not in ["true", "false", "nil"] and right not in ["true", "false", "nil"]:
                    return str(left) + str(right)
                else:
                    self.reportError("string")
            elif node.operator in [ '>', '<', '>=', '<=']:
                if (not isinstance(left, int) and not isinstance(left, float) )or (not isinstance(right, int) and not isinstance(right, float)):
                    self.reportError("binary")
                if node.operator == '>':
                    return "true" if left > right else "false"
                elif node.operator == '<':
                    return "true" if left < right else "false"
                elif node.operator == '>=':
                    return "true" if left >= right else "false"
                elif node.operator == '<=':
                    return "true" if left <= right else "false"
            elif node.operator in ['==', '!=']:
                if node.operator == '==':
                    return "true" if left == right else "false"
                else:
                    return "true" if left != right else "false"
        elif isinstance(node, Variable):
            return self.environment.get(node.name)
        elif isinstance(node, Assign):
            value = self.interpret(node.value)
            self.environment.assign(node.name, value)
            return value
        elif isinstance(node, Logical):
            left = self.interpret(node.left)
            if node.operator.tokenType == "OR":
                if not (not left or left == "false"): # exit if already true
                    return left
            else: # AND
                if not left or left == "false": # exit if already false
                    return left
            return self.interpret(node.right)
                
        # -------------- statements ------------------
        elif isinstance(node, Print):
            val = self.interpret(node.expression)
            if val is None:
                print("nil")
            elif isinstance(val, bool):
                print("true" if val else "false")
            elif isinstance(val, float):
                if val.is_integer():
                    print(int(val))
                else:
                    print(val)
            else:
                print(val)
        elif isinstance(node, Var):
            value = None
            if node.initialiser is not None:
                value = self.interpret(node.initialiser)
            self.environment.define(node.name, value)
            return None
        elif isinstance(node, Expression):
            return self.interpret(node.expression)
        elif isinstance(node, Block):
            self.executeBlock(node.stmts, Environment(self.environment))
            return None
        elif isinstance(node, If):
            val = self.interpret(node.condition)
            if val and val != "false": # if any true val
                self.interpret(node.thenBranch)
            elif node.elseBranch is not None:
                self.interpret(node.elseBranch)
            return None

    def executeBlock(self, stmts: list, env: Environment):
        previous: Environment = self.environment
        try:
            self.environment = env
            for stmt in stmts:
                self.interpret(stmt)
        finally:
            self.environment = previous

    def reportError(self, type):
        self.hadError = True
        if type == "unary":
            print("Operand must be a number.", file=sys.stderr)
        elif type == "binary":
            print("Operands must be numbers.", file=sys.stderr)
        elif type == "string":
            print("Operands must be two numbers or two strings.", file=sys.stderr)
        exit(70)