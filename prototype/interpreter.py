"""
B.E.L. Prototype Interpreter + Borrow Checker Integration

Enhanced version with:
- Basic borrow checking simulation
- Struct support (as dicts)
- Assignments
- Better control flow
- Result/Option simulation hooks
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from parser import (
    Program, Function, Struct, Enum, Expr, Stmt, Block,
    Literal, Identifier, BinaryOp, Call, IfExpr, ReturnExpr,
    LetStmt, ExprStmt, AssignStmt, WhileExpr, ForExpr, LoopExpr
)
from borrow_checker import BorrowChecker

class InterpreterError(Exception):
    pass

class Environment:
    def __init__(self, parent: Optional['Environment'] = None):
        self.values: Dict[str, Any] = {}
        self.parent = parent
    
    def define(self, name: str, value: Any):
        self.values[name] = value
    
    def assign(self, name: str, value: Any):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise InterpreterError(f"Undefined variable '{name}' for assignment")
    
    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise InterpreterError(f"Undefined variable '{name}'")

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.borrow_checker = BorrowChecker()
        self._setup_builtins()
    
    def _setup_builtins(self):
        def bel_print(*args):
            if len(args) == 1:
                print(args[0])
            else:
                fmt = str(args[0])
                result = fmt
                for arg in args[1:]:
                    result = result.replace("{}", str(arg), 1)
                print(result)
        
        self.global_env.define("println", bel_print)
        self.global_env.define("print", lambda *a: print(*a, end=""))

    def interpret(self, program: Program):
        self.borrow_checker.reset()
        
        # Register top-level items
        for item in program.items:
            if isinstance(item, Function):
                self.global_env.define(item.name, item)
            elif isinstance(item, Struct):
                self.global_env.define(item.name, item)
        
        # Find and run main
        main_fn = None
        for item in program.items:
            if isinstance(item, Function) and item.name == "main":
                main_fn = item
                break
        
        if not main_fn:
            print("No main function found.")
            return
        
        try:
            self.call_function(main_fn, [], self.global_env)
        finally:
            if not self.borrow_checker.report_errors():
                print("\n[Prototype] Some borrow rules were violated (educational simulation).")

    def eval_expr(self, expr: Expr, env: Environment) -> Any:
        if isinstance(expr, Literal):
            if expr.type == "int":
                return int(expr.value)
            elif expr.type == "float":
                return float(expr.value)
            elif expr.type == "string":
                return expr.value
            elif expr.type == "bool":
                return expr.value
            elif expr.type == "char":
                return expr.value
            return expr.value
        
        elif isinstance(expr, Identifier):
            # In real version this would check borrows
            return env.get(expr.name)
        
        elif isinstance(expr, BinaryOp):
            if expr.op == ".":
                # Field access (structs simulated as dicts)
                left = self.eval_expr(expr.left, env)
                field = expr.right.name if hasattr(expr.right, 'name') else str(expr.right)
                if isinstance(left, dict):
                    return left.get(field)
                return getattr(left, field, None)
            
            left = self.eval_expr(expr.left, env)
            right = self.eval_expr(expr.right, env)
            
            ops = {
                '+': lambda a,b: a + b,
                '-': lambda a,b: a - b,
                '*': lambda a,b: a * b,
                '/': lambda a,b: a / b if isinstance(a, float) or isinstance(b, float) else a // b,
                '%': lambda a,b: a % b,
                '==': lambda a,b: a == b,
                '!=': lambda a,b: a != b,
                '<': lambda a,b: a < b,
                '>': lambda a,b: a > b,
                '<=': lambda a,b: a <= b,
                '>=': lambda a,b: a >= b,
                '&&': lambda a,b: bool(a) and bool(b),
                '||': lambda a,b: bool(a) or bool(b),
            }
            if expr.op in ops:
                return ops[expr.op](left, right)
            else:
                raise InterpreterError(f"Unknown binary op: {expr.op}")
        
        elif isinstance(expr, Call):
            callee = self.eval_expr(expr.callee, env)
            args = [self.eval_expr(arg, env) for arg in expr.args]
            
            if callable(callee):
                return callee(*args)
            elif isinstance(callee, Function):
                return self.call_function(callee, args, env)
            else:
                raise InterpreterError(f"Cannot call non-function: {callee}")
        
        elif isinstance(expr, Block):
            self.borrow_checker.enter_scope()
            block_env = Environment(parent=env)
            result = None
            for stmt in expr.statements:
                result = self.exec_stmt(stmt, block_env)
            if expr.expr:
                result = self.eval_expr(expr.expr, block_env)
            self.borrow_checker.exit_scope()
            return result
        
        elif isinstance(expr, IfExpr):
            cond = self.eval_expr(expr.condition, env)
            if cond:
                return self.eval_expr(expr.then_block, env)
            elif expr.else_block:
                return self.eval_expr(expr.else_block, env)
            return None
        
        elif isinstance(expr, ReturnExpr):
            val = self.eval_expr(expr.expr, env) if expr.expr else None
            raise ReturnValue(val)
        
        elif isinstance(expr, WhileExpr):
            while self.eval_expr(expr.condition, env):
                self.eval_expr(expr.body, env)
            return None
        
        elif isinstance(expr, ForExpr):
            iterable = self.eval_expr(expr.iterable, env)
            if isinstance(iterable, range):
                for i in iterable:
                    self.borrow_checker.enter_scope()
                    loop_env = Environment(parent=env)
                    loop_env.define(expr.pattern, i)
                    self.eval_expr(expr.body, loop_env)
                    self.borrow_checker.exit_scope()
            return None
        
        elif isinstance(expr, LoopExpr):
            try:
                while True:
                    self.eval_expr(expr.body, env)
            except BreakException:
                pass
            return None
        
        else:
            raise InterpreterError(f"Unhandled expression: {type(expr)}")
    
    def exec_stmt(self, stmt: Stmt, env: Environment):
        if isinstance(stmt, LetStmt):
            value = self.eval_expr(stmt.value, env) if stmt.value else None
            env.define(stmt.pattern, value)
            self.borrow_checker.declare(stmt.pattern)
            # In real version: record ownership
            return value
        
        elif isinstance(stmt, AssignStmt):
            value = self.eval_expr(stmt.value, env)
            if isinstance(stmt.target, Identifier):
                name = stmt.target.name
                # Simulate borrow check for assignment
                self.borrow_checker.check_assignment(name, stmt.line, stmt.column)
                env.assign(name, value)
            return value
        
        elif isinstance(stmt, ExprStmt):
            return self.eval_expr(stmt.expr, env)
        
        else:
            raise InterpreterError(f"Unhandled stmt: {type(stmt)}")
    
    def call_function(self, fn: Function, args: List[Any], caller_env: Environment) -> Any:
        if len(args) != len(fn.params):
            raise InterpreterError(f"{fn.name} expects {len(fn.params)} args, got {len(args)}")
        
        fn_env = Environment(parent=self.global_env)
        self.borrow_checker.enter_scope()
        
        for param, arg in zip(fn.params, args):
            fn_env.define(param.name, arg)
            self.borrow_checker.declare(param.name)
        
        try:
            result = self.eval_expr(fn.body, fn_env)
            return result
        except ReturnValue as ret:
            return ret.value
        finally:
            self.borrow_checker.exit_scope()

@dataclass
class ReturnValue(Exception):
    value: Any

class BreakException(Exception):
    pass

def run_bel(source: str, filename: str = "<stdin>"):
    from parser import parse
    program = parse(source, filename)
    interp = Interpreter()
    interp.interpret(program)
