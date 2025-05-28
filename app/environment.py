from app.tokeniser import Token

class Environment:
    def __init__(self):
        self.values = {}

    def define(self, name: str, value):
        self.values[name.lexeme] = value

    def get(self, name: Token): # returns value
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        raise RuntimeError(f"Undefined variable '{name.lexeme}'.")
        