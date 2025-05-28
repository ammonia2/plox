# Lox Interpreter made in Python

## Resources used for assistance

> Lox is not a real world language! It is made up by the author of the book mentioned below.

- [Crafting Interpreters](https://craftinginterpreters.com/) by Robert Nystrom
- [CodeCrafters](https://app.codecrafters.io/courses/interpreter/) for automated tests

## Code Structure

- `app/`

  - `main.py`: executes all the evaluate, parse, tokenize and other instructions after scanning the code provided
  - `scanner.py`: tokenises all the code provided
  - `tokeniser.py`: contains the `Token` class with token utility functions
  - `parser.py`: parses all the tokens created by tokeniser to conver to Abstract Syntax Tree (AST)
  - `visitor.py`: helper abstract classes (Binary, Grouping, Literal, Unary) for `parser.py` in creation of ASTs
  - `interpreter.py`: evaluates the ASTs and produces output or identifies error based on the code

## Usage Examples

Running main.py requires 3 arguments:`<br>`

- *filename*
- *command (tokenize, parse, etc.)*
- *code path (with .lox extension)*

Example command: `python -m main.py tokenize script.lox` or `./your_program.sh tokenize script.lox`

## Errors Handled

1. Lexical Errors (Scanner Level)

   - Unexpected characters
   - Unterminated strings
   - Invalid number formats
2. Syntax Errors (Parser Level)

   - Missing expressions
   - Unmatched parentheses
   - Invalid token sequences
3. Runtime Errors (Interpreter Level)

   - Type errors for unary operators
   - Type errors for binary operators
   - String concatenation errors

### Exit Codes

- **65**: Lexical or syntax errors
- **70**: Runtime errors

## Requirements

Any stable Python version `<br><br>`

**Libraries:**`<br>`

- sys
- abc (Abstract Base Class)

> This is a project I am working on and off when I get the time to, so it is not complete by any means.
