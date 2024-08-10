import sys
from app.tokeniser import Token

class Scanner:
    source :str # raw source code string
    tokenss: Token = []
    lineNum: int = 1
    start: int = 0
    current: int =0
    hadError = False
    command: str = ""

    def __init__(self, content:str):
        self.source = content

    def addToken(self, token:Token):
        self.tokenss.append(token)

    def createTokens(self, cmd):
        self.command = cmd
        while (self.isAtEnd() != True):
            self.start = self.current
            self.scanToken()

        self.tokenss.append(Token("EOF", "", "null", self.lineNum))
        if self.command == "tokenize":    
            print("EOF  null")

    def scanToken(self):
        char = self.source[self.start]
        next_char = self.source[self.start+1] if (self.start+1 < len(self.source)) else ''
        char_combo = char +next_char
        floatAdded =False
        if (char_combo == '//'):
            self.eoline()
        elif self.isDigit(char):
            c= char
            numVal = ""
            while(self.isAtEnd()==False and  self.isDigit(c)):
                numVal+=c
                self.current+=1
                c = self.source[self.current] if (self.isAtEnd()==False) else ''
            
            if (c=='.' and self.current+1 < len(self.source) and self.isDigit(self.source[self.current+1]) ):
                numVal+=c
                self.current+=1
                c= self.source[self.current]
                while(self.isAtEnd()==False and  self.isDigit(c)):
                    numVal+=c
                    self.current+=1
                    c = self.source[self.current] if (self.isAtEnd()==False) else ''
            else:
                numVal += '.0'
                floatAdded= True

            if (floatAdded): #manually added .0 check
                numVal2 =int(numVal[:-2])
            else:
                try:
                    numVal2 = int(numVal)
                except ValueError:
                    numVal2 = float(numVal)
            newToken = Token("NUMBER", numVal2, float(numVal), self.lineNum)
            self.addToken(newToken)
            if (self.command == "tokenize"):
                print(newToken.tokenisedForm())
        elif self.isAlpha(char):
            identifierVal = ""
            c = char
            while (not self.isAtEnd() and  self.isAlphaNumeric(c)):
                identifierVal+=c
                self.current +=1
                c = self.source[self.current] if (not self.isAtEnd()) else ''
            if identifierVal in keywords:
                newToken = Token(keywords[identifierVal], identifierVal, "null", self.lineNum)
            else:
                newToken = Token("IDENTIFIER", identifierVal, "null", self.lineNum)
            if (self.command == "tokenize"):
                print(newToken.tokenisedForm())
            self.addToken(newToken)
        elif (char == '"'):
            strVal = "\""
            endFound = False
            self.current+=1
            while (self.isAtEnd()==False and self.source[self.current] != '"'):
                strVal += self.source[self.current]
                if (self.source[self.current] == '\n'): self.lineNum +=1
                self.current+=1
                if (self.isAtEnd()==False and self.source[self.current]=='"'): endFound = True
            strVal += '\"'
            if (self.isAtEnd() and endFound==False):
                self.reportError(self.lineNum, "Unterminated string.")
                return

            self.current+=1
            newToken = Token("STRING", strVal, strVal[1:-1], self.lineNum)
            self.addToken(newToken)
            if (self.command == "tokenize"):
                print(newToken.tokenisedForm())        

        elif (char_combo in tokenDict):
            newToken = Token(tokenDict[char_combo], char_combo, "null", self.lineNum)
            if (self.command == "tokenize"):
                print(newToken.tokenisedForm())
            self.addToken(newToken)
            self.current+=2
        elif char in tokenDict:
            newToken = Token(tokenDict[char], char, "null", self.lineNum)
            if (self.command == "tokenize"):
                print(newToken.tokenisedForm())
            self.addToken(newToken)
            self.current+=1
        elif char==' ' or char == '\n' or char == '\t':
            self.current+=1
            if (char == '\n'): self.lineNum+=1
        else:
            self.reportError(self.lineNum,"Unexpected character", char)
            self.current+=1

    def eoline(self):
        while (self.isAtEnd()!=True and self.source[self.current] != '\n'):
            self.current+=1

    def isDigit(self, c) -> bool:
        return (c >= '0' and c <= '9')

    def isAlpha(self, c) -> bool:
        return ((c>='a' and c<='z') or (c>='A' and c<='Z') or c=='_')

    def isAlphaNumeric(self, c)-> bool:
        return (self.isAlpha(c) or self.isDigit(c))

    def isAtEnd(self) -> bool:
        return (self.current >= len(self.source))

    def reportError(self, lineNum, errType, char=''):
        self.hadError = True
        if errType=="Unexpected character":
            print(f"[line {lineNum}] Error: {errType}: {char}", file=sys.stderr)
        else:
            print(f"[line {lineNum}] Error: {errType}", file=sys.stderr)

tokenDict = {
    '(': "LEFT_PAREN",
    ')': "RIGHT_PAREN",
    '{': "LEFT_BRACE",
    '}': "RIGHT_BRACE",
    '*': "STAR",
    '.': "DOT",
    ',': "COMMA",
    '+': "PLUS",
    '-': "MINUS",
    ';': "SEMICOLON",
    '=': "EQUAL",
    '==': "EQUAL_EQUAL",
    '!': "BANG",
    '!=': "BANG_EQUAL",
    '<': "LESS",
    '<=': "LESS_EQUAL",
    '>': "GREATER",
    '>=': "GREATER_EQUAL",
    '/': "SLASH",
}

keywords = {
    "and": "AND",
    "class": "CLASS",
    "else": "ELSE",
    "false": "FALSE",
    "for": "FOR",
    "fun": "FUN",
    "if": "IF",
    "nil": "NIL",
    "or": "OR",
    "print": "PRINT",
    "return": "RETURN",
    "super": "SUPER",
    "this": "THIS",
    "true": "TRUE",
    "var": "VAR",
    "while": "WHILE"
}