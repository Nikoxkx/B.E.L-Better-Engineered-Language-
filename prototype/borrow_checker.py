"""
B.E.L. Prototype Borrow Checker (Simulation)

A simplified borrow checker for the prototype.
It demonstrates the core rules:
- One owner
- Moves invalidate previous owner
- Shared (&) vs exclusive (&mut) borrows
- Basic lifetime / scope checking

This is educational and intentionally simplified.
Real implementation lives in the compiler (see docs/ownership-model.md).
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum, auto

class BorrowKind(Enum):
    Shared = auto()
    Mutable = auto()

@dataclass
class BorrowInfo:
    kind: BorrowKind
    scope_level: int
    var_name: str

@dataclass
class VariableState:
    owned: bool = True
    moved: bool = False
    borrows: List[BorrowInfo] = field(default_factory=list)

class BorrowChecker:
    def __init__(self):
        self.scopes: List[Dict[str, VariableState]] = [{}]  # stack of scopes
        self.errors: List[str] = []
        self.scope_level = 0

    def enter_scope(self):
        self.scopes.append({})
        self.scope_level += 1

    def exit_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
            self.scope_level -= 1

    def current_scope(self) -> Dict[str, VariableState]:
        return self.scopes[-1]

    def declare(self, name: str):
        self.current_scope()[name] = VariableState()

    def move(self, name: str, line: int, col: int) -> bool:
        state = self._find_var(name)
        if not state:
            self.errors.append(f"[{line}:{col}] Use of undeclared variable '{name}'")
            return False
        if state.moved:
            self.errors.append(f"[{line}:{col}] Use of moved value '{name}'")
            return False
        
        # Check for active borrows
        if state.borrows:
            self.errors.append(f"[{line}:{col}] Cannot move '{name}' while borrowed")
            return False
        
        state.moved = True
        state.owned = False
        return True

    def borrow(self, name: str, mutable: bool, line: int, col: int) -> bool:
        state = self._find_var(name)
        if not state:
            self.errors.append(f"[{line}:{col}] Use of undeclared variable '{name}'")
            return False
        if state.moved:
            self.errors.append(f"[{line}:{col}] Use of moved value '{name}'")
            return False

        kind = BorrowKind.Mutable if mutable else BorrowKind.Shared

        # Check borrow rules
        has_mutable = any(b.kind == BorrowKind.Mutable for b in state.borrows)
        has_shared = any(b.kind == BorrowKind.Shared for b in state.borrows)

        if kind == BorrowKind.Mutable:
            if has_mutable or has_shared:
                self.errors.append(f"[{line}:{col}] Cannot borrow '{name}' mutably while already borrowed")
                return False
        else:  # Shared
            if has_mutable:
                self.errors.append(f"[{line}:{col}] Cannot borrow '{name}' while mutably borrowed")
                return False

        state.borrows.append(BorrowInfo(kind=kind, scope_level=self.scope_level, var_name=name))
        return True

    def end_borrow(self, name: str):
        state = self._find_var(name)
        if state:
            # Remove borrows from current scope level (simplified)
            state.borrows = [b for b in state.borrows if b.scope_level < self.scope_level]

    def _find_var(self, name: str) -> Optional[VariableState]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def check_assignment(self, name: str, line: int, col: int) -> bool:
        state = self._find_var(name)
        if not state:
            self.errors.append(f"[{line}:{col}] Assignment to undeclared '{name}'")
            return False
        if state.moved:
            self.errors.append(f"[{line}:{col}] Assignment to moved value '{name}'")
            return False
        if any(b.kind == BorrowKind.Shared for b in state.borrows):
            self.errors.append(f"[{line}:{col}] Cannot assign to '{name}' while borrowed")
            return False
        return True

    def report_errors(self):
        if self.errors:
            print("\n=== Borrow Checker Errors (Prototype Simulation) ===")
            for e in self.errors:
                print(e)
            return False
        return True

    def reset(self):
        self.scopes = [{}]
        self.errors = []
        self.scope_level = 0
