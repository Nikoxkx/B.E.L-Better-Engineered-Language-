"""
B.E.L. Lexer (Prototype)

A hand-written lexer for the B.E.L. programming language.
This is part of the initial prototype to validate the language design and grammar.
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional, Iterator

class TokenType(Enum):
    # Keywords
    FN = auto()
    LET = auto()
    CONST = auto()
    STRUCT = auto()
    ENUM = auto()
    TRAIT = auto()
    IMPL = auto()
    MOD = auto()
    USE = auto()
    IMPORT = auto()
    PUB = auto()
    MUT = auto()
    REF = auto()
    MOVE = auto()
    ASYNC = auto()
    AWAIT = auto()
    MATCH = auto()
    IF = auto()
    ELSE = auto()
    LOOP = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    UNSAFE = auto()
    WHERE = auto()
    TYPE = auto()
    STATIC = auto()
    EXTERN = auto()
    SIZEOF = auto()
    ALIGNOF = auto()
    CONSTEXPR = auto()
    MACRO = auto()
    YIELD = auto()
    SPAWN = auto()
    BOX = auto()
    TRUE = auto()
    FALSE = auto()
    AS = auto()
    
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    CHAR = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Operators and Punctuation
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    EQ = auto()
    EQEQ = auto()
    NEQ = auto()
    LT = auto()
    GT = auto()
    LTE = auto()
    GTE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    AMP = auto()
    PIPE = auto()
    CARET = auto()
    LSHIFT = auto()
    RSHIFT = auto()
    PLUS_EQ = auto()
    MINUS_EQ = auto()
    STAR_EQ = auto()
    SLASH_EQ = auto()
    PERCENT_EQ = auto()
    
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    DOT = auto()
    ARROW = auto()
    FAT_ARROW = auto()
    DOTDOT = auto()
    DOTDOTEQ = auto()
    QUESTION = auto()
    BANG = auto()
    
    # Special
    EOF = auto()
    COMMENT = auto()
    DOC_COMMENT = auto()

KEYWORDS = {
    'fn': TokenType.FN,
    'let': TokenType.LET,
    'const': TokenType.CONST,
    'struct': TokenType.STRUCT,
    'enum': TokenType.ENUM,
    'trait': TokenType.TRAIT,
    'impl': TokenType.IMPL,
    'mod': TokenType.MOD,
    'use': TokenType.USE,
    'import': TokenType.IMPORT,
    'pub': TokenType.PUB,
    'mut': TokenType.MUT,
    'ref': TokenType.REF,
    'move': TokenType.MOVE,
    'async': TokenType.ASYNC,
    'await': TokenType.AWAIT,
    'match': TokenType.MATCH,
    'if': TokenType.IF,
    'else': TokenType.ELSE,
    'loop': TokenType.LOOP,
    'while': TokenType.WHILE,
    'for': TokenType.FOR,
    'in': TokenType.IN,
    'break': TokenType.BREAK,
    'continue': TokenType.CONTINUE,
    'return': TokenType.RETURN,
    'unsafe': TokenType.UNSAFE,
    'where': TokenType.WHERE,
    'type': TokenType.TYPE,
    'static': TokenType.STATIC,
    'extern': TokenType.EXTERN,
    'sizeof': TokenType.SIZEOF,
    'alignof': TokenType.ALIGNOF,
    'constexpr': TokenType.CONSTEXPR,
    'macro': TokenType.MACRO,
    'yield': TokenType.YIELD,
    'spawn': TokenType.SPAWN,
    'box': TokenType.BOX,
    'true': TokenType.TRUE,
    'false': TokenType.FALSE,
    'as': TokenType.AS,
}

@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int
    length: int = 1

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, line={self.line}, col={self.column})"

class LexerError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"Lexer error at line {line}, column {column}: {message}")
        self.line = line
        self.column = column

class Lexer:
    def __init__(self, source: str, filename: str = "<stdin>"):
        self.source = source
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
    
    def current_char(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        if self.pos + offset >= len(self.source):
            return None
        return self.source[self.pos + offset]
    
    def advance(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        char = self.source[self.pos]
        self.pos += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        if self.current_char() == '/' and self.peek() == '/':
            # Line comment
            start_line = self.line
            self.advance()  # /
            self.advance()  # /
            is_doc = False
            if self.current_char() == '/':
                is_doc = True
                self.advance()
            while self.current_char() and self.current_char() != '\n':
                self.advance()
            return True
        elif self.current_char() == '/' and self.peek() == '*':
            # Block comment (nestable for now, simple version)
            self.advance()  # /
            self.advance()  # *
            depth = 1
            while depth > 0 and self.current_char():
                if self.current_char() == '/' and self.peek() == '*':
                    self.advance()
                    self.advance()
                    depth += 1
                elif self.current_char() == '*' and self.peek() == '/':
                    self.advance()
                    self.advance()
                    depth -= 1
                else:
                    self.advance()
            return True
        return False
    
    def read_identifier(self) -> str:
        start = self.pos
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            self.advance()
        return self.source[start:self.pos]
    
    def read_number(self) -> tuple:
        start = self.pos
        is_float = False
        
        # Handle hex, bin, oct
        if self.current_char() == '0' and self.peek() in 'xXbBoO':
            prefix = self.advance() + self.advance()
            while self.current_char() and self.current_char().isalnum():
                self.advance()
            value = self.source[start:self.pos]
            return TokenType.INTEGER, value
        
        while self.current_char() and self.current_char().isdigit():
            self.advance()
        
        if self.current_char() == '.' and self.peek() and self.peek().isdigit():
            is_float = True
            self.advance()  # .
            while self.current_char() and self.current_char().isdigit():
                self.advance()
        
        if self.current_char() and self.current_char().lower() == 'e':
            is_float = True
            self.advance()
            if self.current_char() in '+-':
                self.advance()
            while self.current_char() and self.current_char().isdigit():
                self.advance()
        
        # Suffixes like i32, f64, u64 etc.
        if self.current_char() and self.current_char().isalpha():
            while self.current_char() and self.current_char().isalnum():
                self.advance()
        
        value = self.source[start:self.pos]
        return (TokenType.FLOAT if is_float else TokenType.INTEGER), value
    
    def read_string(self) -> str:
        quote = self.advance()  # consume opening quote
        start = self.pos
        value = ""
        
        while self.current_char() and self.current_char() != quote:
            if self.current_char() == '\\':
                self.advance()
                escaped = self.advance()
                if escaped == 'n':
                    value += '\n'
                elif escaped == 'r':
                    value += '\r'
                elif escaped == 't':
                    value += '\t'
                elif escaped == '"':
                    value += '"'
                elif escaped == "'":
                    value += "'"
                elif escaped == '\\':
                    value += '\\'
                elif escaped == '0':
                    value += '\0'
                elif escaped == 'u':
                    if self.current_char() == '{':
                        self.advance()
                        hex_start = self.pos
                        while self.current_char() and self.current_char() != '}':
                            self.advance()
                        hex_val = self.source[hex_start:self.pos]
                        try:
                            value += chr(int(hex_val, 16))
                        except:
                            value += f'\\u{{{hex_val}}}'
                        self.advance()
                    else:
                        value += '\\u'
                else:
                    value += '\\' + escaped
            else:
                value += self.advance()
        
        if self.current_char() != quote:
            raise LexerError("Unterminated string literal", self.line, self.column)
        self.advance()  # consume closing quote
        return value
    
    def read_char(self) -> str:
        self.advance()  # '
        if self.current_char() == '\\':
            self.advance()
            escaped = self.advance()
            char_val = {
                'n': '\n', 'r': '\r', 't': '\t', 
                '"': '"', "'": "'", '\\': '\\', '0': '\0'
            }.get(escaped, escaped)
            if self.current_char() != "'":
                raise LexerError("Unterminated char literal", self.line, self.column)
            self.advance()
            return char_val
        else:
            char_val = self.advance()
            if self.current_char() != "'":
                raise LexerError("Unterminated char literal", self.line, self.column)
            self.advance()
            return char_val
    
    def tokenize(self) -> List[Token]:
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.column = 1
        
        while self.pos < len(self.source):
            self.skip_whitespace()
            if self.pos >= len(self.source):
                break
            
            start_line = self.line
            start_col = self.column
            char = self.current_char()
            
            if self.skip_comment():
                continue
            
            if char.isalpha() or char == '_':
                ident = self.read_identifier()
                token_type = KEYWORDS.get(ident, TokenType.IDENTIFIER)
                self.tokens.append(Token(token_type, ident, start_line, start_col))
                continue
            
            if char.isdigit():
                tok_type, value = self.read_number()
                self.tokens.append(Token(tok_type, value, start_line, start_col))
                continue
            
            if char == '"':
                value = self.read_string()
                self.tokens.append(Token(TokenType.STRING, value, start_line, start_col))
                continue
            
            if char == "'":
                value = self.read_char()
                self.tokens.append(Token(TokenType.CHAR, value, start_line, start_col))
                continue
            
            two_char = char + (self.peek() or '')
            two_char_map = {
                '==': TokenType.EQEQ,
                '!=': TokenType.NEQ,
                '<=': TokenType.LTE,
                '>=': TokenType.GTE,
                '&&': TokenType.AND,
                '||': TokenType.OR,
                '->': TokenType.ARROW,
                '=>': TokenType.FAT_ARROW,
                '..': TokenType.DOTDOT,
                '..=': TokenType.DOTDOTEQ,
                '+=': TokenType.PLUS_EQ,
                '-=': TokenType.MINUS_EQ,
                '*=': TokenType.STAR_EQ,
                '/=': TokenType.SLASH_EQ,
                '%=': TokenType.PERCENT_EQ,
                '<<': TokenType.LSHIFT,
                '>>': TokenType.RSHIFT,
            }
            if two_char in two_char_map:
                self.advance()
                self.advance()
                self.tokens.append(Token(two_char_map[two_char], two_char, start_line, start_col))
                continue
            
            single_map = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.STAR,
                '/': TokenType.SLASH,
                '%': TokenType.PERCENT,
                '=': TokenType.EQ,
                '<': TokenType.LT,
                '>': TokenType.GT,
                '&': TokenType.AMP,
                '|': TokenType.PIPE,
                '^': TokenType.CARET,
                '!': TokenType.BANG,
                '?': TokenType.QUESTION,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                '[': TokenType.LBRACKET,
                ']': TokenType.RBRACKET,
                ',': TokenType.COMMA,
                ';': TokenType.SEMICOLON,
                ':': TokenType.COLON,
                '.': TokenType.DOT,
            }
            
            if char in single_map:
                self.advance()
                self.tokens.append(Token(single_map[char], char, start_line, start_col))
                continue
            
            raise LexerError(f"Unexpected character: {char!r}", start_line, start_col)
        
        self.tokens.append(Token(TokenType.EOF, "", self.line, self.column))
        return self.tokens

def lex(source: str, filename: str = "<stdin>") -> List[Token]:
    lexer = Lexer(source, filename)
    return lexer.tokenize()
