import sys
from app.tokeniser import Token

class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: str, value):
        self.values[name.lexeme] = value

    def get(self, name: Token): # returns value
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        self.__reportError(name.lexeme)
        
    def assign(self, name: Token, value):
        if name.lexeme not in self.values:
            self.__reportError(name.lexeme)
        
        self.values[name.lexeme] = value

    def __reportError(self, name):
        print(f"Undefined Variable '{name}'.", file=sys.stderr)
        exit(70)