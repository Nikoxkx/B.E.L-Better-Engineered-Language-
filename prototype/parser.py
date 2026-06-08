# [Same content as before but with improved block parsing to handle returns and statements inside if/while etc.]

"""
B.E.L. Parser (Prototype) - Improved

Improved block parsing and statement handling.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Any, Union
from lexer import Token, TokenType, lex

@dataclass
class ASTNode:
    line: int
    column: int

@dataclass
class Program(ASTNode):
    items: List['Item'] = field(default_factory=list)

@dataclass
class Item(ASTNode):
    pass

@dataclass
class Function(Item):
    name: str
    params: List['Param']
    return_type: Optional[str]
    body: 'Block'
    is_async: bool = False
    visibility: str = "private"

@dataclass
class Param(ASTNode):
    name: str
    type: str
    is_mut: bool = False

@dataclass
class Struct(Item):
    name: str
    fields: List['StructField']
    visibility: str = "private"

@dataclass
class StructField(ASTNode):
    name: str
    type: str
    visibility: str = "private"

@dataclass
class Enum(Item):
    name: str
    variants: List['EnumVariant']

@dataclass
class EnumVariant(ASTNode):
    name: str
    data: Optional[List[str]] = None

@dataclass
class Use(Item):
    path: str

@dataclass
class Expr(ASTNode):
    pass

@dataclass
class Literal(Expr):
    value: Any
    type: str

@dataclass
class Identifier(Expr):
    name: str

@dataclass
class BinaryOp(Expr):
    left: Expr
    op: str
    right: Expr

@dataclass
class UnaryOp(Expr):
    op: str
    expr: Expr

@dataclass
class Call(Expr):
    callee: Expr
    args: List[Expr]

@dataclass
class Block(Expr):
    statements: List['Stmt']
    expr: Optional[Expr] = None

@dataclass
class IfExpr(Expr):
    condition: Expr
    then_block: Block
    else_block: Optional[Union[Block, 'IfExpr']] = None

@dataclass
class MatchExpr(Expr):
    expr: Expr
    arms: List['MatchArm']

@dataclass
class MatchArm(ASTNode):
    pattern: str
    guard: Optional[Expr]
    body: Expr

@dataclass
class LoopExpr(Expr):
    body: Block

@dataclass
class WhileExpr(Expr):
    condition: Expr
    body: Block

@dataclass
class ForExpr(Expr):
    pattern: str
    iterable: Expr
    body: Block

@dataclass
class ReturnExpr(Expr):
    expr: Optional[Expr] = None

@dataclass
class AwaitExpr(Expr):
    expr: Expr

@dataclass
class Stmt(ASTNode):
    pass

@dataclass
class LetStmt(Stmt):
    pattern: str
    type: Optional[str]
    value: Optional[Expr]
    is_mut: bool = False

@dataclass
class ExprStmt(Stmt):
    expr: Expr

@dataclass
class AssignStmt(Stmt):
    target: Expr
    value: Expr

class ParserError(Exception):
    def __init__(self, message: str, token: Optional[Token] = None):
        if token:
            super().__init__(f"Parser error at line {token.line}, col {token.column}: {message}")
        else:
            super().__init__(f"Parser error: {message}")

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
    
    def current(self) -> Token:
        return self.tokens[self.pos]
    
    def peek(self, offset: int = 1) -> Token:
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else self.tokens[-1]
    
    def advance(self) -> Token:
        tok = self.current()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return tok
    
    def expect(self, token_type: TokenType, message: Optional[str] = None) -> Token:
        if self.current().type == token_type:
            return self.advance()
        msg = message or f"Expected {token_type.name}, got {self.current().type.name}"
        raise ParserError(msg, self.current())
    
    def match(self, *types: TokenType) -> bool:
        if self.current().type in types:
            self.advance()
            return True
        return False
    
    def parse_program(self) -> Program:
        items = []
        while self.current().type != TokenType.EOF:
            item = self.parse_item()
            if item is not None:
                items.append(item)
        return Program(items=items, line=1, column=1)
    
    def parse_item(self) -> Optional[Item]:
        visibility = "private"
        if self.match(TokenType.PUB):
            visibility = "pub"
        
        tok = self.current()
        
        if tok.type == TokenType.FN or (tok.type == TokenType.ASYNC and self.peek().type == TokenType.FN):
            return self.parse_function(visibility)
        elif tok.type == TokenType.STRUCT:
            return self.parse_struct(visibility)
        elif tok.type == TokenType.ENUM:
            return self.parse_enum(visibility)
        elif tok.type in (TokenType.USE, TokenType.IMPORT):
            return self.parse_use()
        elif tok.type == TokenType.CONST:
            self.advance()
            depth = 0
            while self.current().type != TokenType.EOF:
                if self.current().type == TokenType.LBRACE:
                    depth += 1
                elif self.current().type == TokenType.RBRACE:
                    depth -= 1
                if self.current().type == TokenType.SEMICOLON and depth == 0:
                    break
                self.advance()
            self.match(TokenType.SEMICOLON)
            return None
        else:
            # Skip unknown for robustness in prototype
            self.advance()
            return None
    
    def parse_function(self, visibility: str) -> Function:
        is_async = self.match(TokenType.ASYNC)
        self.expect(TokenType.FN)
        name_tok = self.expect(TokenType.IDENTIFIER)
        name = name_tok.value
        self.expect(TokenType.LPAREN)
        params = self.parse_param_list()
        self.expect(TokenType.RPAREN)
        
        return_type = None
        if self.match(TokenType.ARROW):
            return_type = self.parse_type()
        
        body = self.parse_block()
        return Function(name=name, params=params, return_type=return_type, body=body,
                        is_async=is_async, visibility=visibility, line=name_tok.line, column=name_tok.column)
    
    def parse_param_list(self) -> List[Param]:
        params = []
        while self.current().type != TokenType.RPAREN:
            is_mut = self.match(TokenType.MUT)
            pat = self.expect(TokenType.IDENTIFIER)
            self.expect(TokenType.COLON)
            typ = self.parse_type()
            params.append(Param(name=pat.value, type=typ, is_mut=is_mut, line=pat.line, column=pat.column))
            if not self.match(TokenType.COMMA):
                break
        return params
    
    def parse_type(self) -> str:
        parts = []
        if self.match(TokenType.AMP):
            parts.append("&")
            if self.match(TokenType.MUT):
                parts.append("mut ")
        elif self.match(TokenType.STAR):
            parts.append("*")
            if self.match(TokenType.CONST):
                parts.append("const ")
            elif self.match(TokenType.MUT):
                parts.append("mut ")
        if self.current().type == TokenType.IDENTIFIER:
            parts.append(self.advance().value)
        elif self.current().type == TokenType.LBRACKET:
            self.advance()
            inner = self.parse_type()
            if self.match(TokenType.SEMICOLON):
                sz = self.expect(TokenType.INTEGER).value
                parts.append(f"[{inner};{sz}]")
            else:
                parts.append(f"[{inner}]")
            self.expect(TokenType.RBRACKET)
        else:
            raise ParserError("Expected type", self.current())
        if self.match(TokenType.LT):
            g = self.parse_type()
            self.expect(TokenType.GT)
            parts.append(f"<{g}>")
        return "".join(parts)
    
    def parse_struct(self, visibility: str) -> Struct:
        self.expect(TokenType.STRUCT)
        name_tok = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.LBRACE)
        fields = []
        while self.current().type != TokenType.RBRACE:
            fvis = "private"
            if self.match(TokenType.PUB):
                fvis = "pub"
            fname = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.COLON)
            ftype = self.parse_type()
            fields.append(StructField(name=fname, type=ftype, visibility=fvis, line=self.current().line, column=self.current().column))
            self.match(TokenType.COMMA)
        self.expect(TokenType.RBRACE)
        return Struct(name=name_tok.value, fields=fields, visibility=visibility, line=name_tok.line, column=name_tok.column)
    
    def parse_enum(self, visibility: str) -> Enum:
        self.expect(TokenType.ENUM)
        name_tok = self.expect(TokenType.IDENTIFIER)
        self.expect(TokenType.LBRACE)
        variants = []
        while self.current().type != TokenType.RBRACE:
            vname = self.expect(TokenType.IDENTIFIER).value
            data = None
            if self.match(TokenType.LPAREN):
                ts = []
                while self.current().type != TokenType.RPAREN:
                    ts.append(self.parse_type())
                    if not self.match(TokenType.COMMA): break
                self.expect(TokenType.RPAREN)
                data = ts
            variants.append(EnumVariant(name=vname, data=data, line=self.current().line, column=self.current().column))
            self.match(TokenType.COMMA)
        self.expect(TokenType.RBRACE)
        return Enum(name=name_tok.value, variants=variants, line=name_tok.line, column=name_tok.column)
    
    def parse_use(self) -> Use:
        self.advance()  # use or import
        parts = []
        while self.current().type == TokenType.IDENTIFIER:
            parts.append(self.advance().value)
            if self.match(TokenType.COLONCOLON) or self.match(TokenType.DOT) or self.match(TokenType.COLON):
                continue
            break
        self.match(TokenType.SEMICOLON)
        return Use(path="::".join(parts) if parts else "*", line=self.current().line, column=self.current().column)
    
    def parse_block(self) -> Block:
        lbrace = self.expect(TokenType.LBRACE)
        stmts = []
        final = None
        while self.current().type not in (TokenType.RBRACE, TokenType.EOF):
            if self.current().type in (TokenType.LET, TokenType.CONST):
                stmts.append(self.parse_let_stmt())
            else:
                e = self.parse_expr()
                if self.match(TokenType.SEMICOLON):
                    stmts.append(ExprStmt(expr=e, line=e.line, column=e.column))
                else:
                    final = e
                    # allow optional semicolon after final expr in blocks
                    self.match(TokenType.SEMICOLON)
                    break
        self.expect(TokenType.RBRACE)
        return Block(statements=stmts, expr=final, line=lbrace.line, column=lbrace.column)
    
    def parse_let_stmt(self) -> LetStmt:
        self.expect(TokenType.LET)
        is_mut = self.match(TokenType.MUT)
        pat = self.expect(TokenType.IDENTIFIER)
        typ = None
        if self.match(TokenType.COLON):
            typ = self.parse_type()
        val = None
        if self.match(TokenType.EQ):
            val = self.parse_expr()
        self.expect(TokenType.SEMICOLON)
        return LetStmt(pattern=pat.value, type=typ, value=val, is_mut=is_mut, line=pat.line, column=pat.column)
    
    def parse_expr(self) -> Expr:
        return self.parse_expr_prec(0)
    
    PRECEDENCE = {'||':1, '&&':2, '==':3,'!=':3,'<':3,'>':3,'<=':3,'>=':3, '+':4,'-':4, '*':5,'/':5,'%':5}
    
    def parse_expr_prec(self, min_prec: int) -> Expr:
        left = self.parse_unary()
        while True:
            op_tok = self.current()
            op_str = op_tok.value
            prec = self.PRECEDENCE.get(op_str, 0)
            if prec < min_prec or op_tok.type not in (TokenType.PLUS,TokenType.MINUS,TokenType.STAR,TokenType.SLASH,TokenType.PERCENT,TokenType.EQEQ,TokenType.NEQ,TokenType.LT,TokenType.GT,TokenType.LTE,TokenType.GTE,TokenType.AND,TokenType.OR):
                break
            self.advance()
            right = self.parse_expr_prec(prec + 1)
            left = BinaryOp(left=left, op=op_str, right=right, line=op_tok.line, column=op_tok.column)
        return left
    
    def parse_unary(self) -> Expr:
        tok = self.current()
        if tok.type in (TokenType.MINUS, TokenType.NOT, TokenType.AMP, TokenType.STAR):
            op = tok.value
            self.advance()
            return UnaryOp(op=op, expr=self.parse_unary(), line=tok.line, column=tok.column)
        return self.parse_primary()
    
    def parse_primary(self) -> Expr:
        tok = self.current()
        if tok.type == TokenType.INTEGER:
            self.advance()
            return Literal(value=tok.value, type="int", line=tok.line, column=tok.column)
        if tok.type == TokenType.FLOAT:
            self.advance()
            return Literal(value=tok.value, type="float", line=tok.line, column=tok.column)
        if tok.type == TokenType.STRING:
            self.advance()
            return Literal(value=tok.value, type="string", line=tok.line, column=tok.column)
        if tok.type == TokenType.CHAR:
            self.advance()
            return Literal(value=tok.value, type="char", line=tok.line, column=tok.column)
        if tok.type == TokenType.TRUE:
            self.advance()
            return Literal(value=True, type="bool", line=tok.line, column=tok.column)
        if tok.type == TokenType.FALSE:
            self.advance()
            return Literal(value=False, type="bool", line=tok.line, column=tok.column)
        if tok.type == TokenType.IDENTIFIER:
            self.advance()
            expr = Identifier(name=tok.value, line=tok.line, column=tok.column)
            while True:
                if self.match(TokenType.LPAREN):
                    args = []
                    while self.current().type != TokenType.RPAREN:
                        args.append(self.parse_expr())
                        if not self.match(TokenType.COMMA): break
                    self.expect(TokenType.RPAREN)
                    expr = Call(callee=expr, args=args, line=tok.line, column=tok.column)
                elif self.match(TokenType.DOT):
                    fld = self.expect(TokenType.IDENTIFIER)
                    expr = BinaryOp(left=expr, op=".", right=Identifier(name=fld.value, line=fld.line, column=fld.column), line=fld.line, column=fld.column)
                else:
                    break
            return expr
        if tok.type == TokenType.LPAREN:
            self.advance()
            e = self.parse_expr()
            self.expect(TokenType.RPAREN)
            return e
        if tok.type == TokenType.LBRACE:
            return self.parse_block()
        if tok.type == TokenType.IF:
            return self.parse_if_expr()
        if tok.type == TokenType.MATCH:
            return self.parse_match_expr()
        if tok.type == TokenType.LOOP:
            self.advance()
            return LoopExpr(body=self.parse_block(), line=tok.line, column=tok.column)
        if tok.type == TokenType.WHILE:
            self.advance()
            cond = self.parse_expr()
            return WhileExpr(condition=cond, body=self.parse_block(), line=tok.line, column=tok.column)
        if tok.type == TokenType.FOR:
            self.advance()
            pat = self.expect(TokenType.IDENTIFIER).value
            self.expect(TokenType.IN)
            it = self.parse_expr()
            return ForExpr(pattern=pat, iterable=it, body=self.parse_block(), line=tok.line, column=tok.column)
        if tok.type == TokenType.RETURN:
            self.advance()
            val = None
            if self.current().type not in (TokenType.SEMICOLON, TokenType.RBRACE, TokenType.EOF):
                val = self.parse_expr()
            return ReturnExpr(expr=val, line=tok.line, column=tok.column)
        if tok.type == TokenType.AWAIT:
            self.advance()
            return AwaitExpr(expr=self.parse_expr(), line=tok.line, column=tok.column)
        raise ParserError(f"Unexpected token in primary: {tok.type.name}", tok)
    
    def parse_if_expr(self) -> IfExpr:
        tok = self.advance()
        cond = self.parse_expr()
        then_b = self.parse_block()
        else_b = None
        if self.match(TokenType.ELSE):
            if self.current().type == TokenType.IF:
                else_b = self.parse_if_expr()
            else:
                else_b = self.parse_block()
        return IfExpr(condition=cond, then_block=then_b, else_block=else_b, line=tok.line, column=tok.column)
    
    def parse_match_expr(self) -> MatchExpr:
        tok = self.advance()
        e = self.parse_expr()
        self.expect(TokenType.LBRACE)
        arms = []
        while self.current().type != TokenType.RBRACE:
            pat = ""
            while self.current().type not in (TokenType.FAT_ARROW, TokenType.IF, TokenType.EOF, TokenType.RBRACE):
                pat += self.advance().value + " "
            pat = pat.strip()
            g = self.parse_expr() if self.match(TokenType.IF) else None
            self.expect(TokenType.FAT_ARROW)
            body = self.parse_expr()
            self.match(TokenType.COMMA)
            arms.append(MatchArm(pattern=pat, guard=g, body=body, line=tok.line, column=tok.column))
        self.expect(TokenType.RBRACE)
        return MatchExpr(expr=e, arms=arms, line=tok.line, column=tok.column)

def parse(source: str, filename: str = "<stdin>") -> Program:
    tokens = lex(source, filename)
    p = Parser(tokens)
    return p.parse_program()
