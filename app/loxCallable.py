from app.interpreter import Interpreter
from abc import ABC, abstractmethod

class LoxCallable(ABC):
    @abstractmethod
    def call( interpreter: Interpreter, arguments: list):
        pass

    @abstractmethod
    def arity():
        pass