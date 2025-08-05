from app.interpreter import Interpreter
from abc import ABC, abstractmethod

class LoxCallable(ABC):
    @abstractmethod
    def call(self, interpreter: Interpreter, arguments: list):
        pass

    @abstractmethod
    def arity(self):
        pass

    def __str__(self):
        pass