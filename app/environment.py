import sys
from app.tokeniser import Token

class Environment:
    def __init__(self, enclosing: 'Environment' = None):
        self.values = {}
        self.enclosing: 'Environment' = enclosing
        
    def define(self, name: str, value):
        if isinstance(name, Token):
            self.values[name.lexeme] = value
        else:
            self.values[name] = value

    def get(self, name: Token): # returns value
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        if self.enclosing != None: return self.enclosing.get(name)

        self.__reportError(name.lexeme)
        
    def assign(self, name: Token, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        
        if self.enclosing !=None:
            self.enclosing.assign(name, value)
            return

        self.__reportError(name.lexeme)

    def __reportError(self, name):
        print(f"Undefined Variable '{name}'.", file=sys.stderr)
        exit(70)