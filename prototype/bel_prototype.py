#!/usr/bin/env python3
"""
B.E.L. Prototype Tool

Design validation prototype for the B.E.L. (Better Engineered Language) programming language.

Usage:
  python prototype/bel_prototype.py lex examples/hello.bel
  python prototype/bel_prototype.py parse examples/hello.bel
  python prototype/bel_prototype.py run examples/hello.bel
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lexer import lex, TokenType
from parser import parse
from interpreter import run_bel

def cmd_lex(args):
    source = Path(args.file).read_text()
    tokens = lex(source, args.file)
    for tok in tokens:
        if tok.type != TokenType.EOF:
            print(f"{tok.type.name:12} {tok.value!r:20} @ {tok.line}:{tok.column}")

def cmd_parse(args):
    source = Path(args.file).read_text()
    program = parse(source, args.file)
    print(f"Parsed B.E.L. program with {len(program.items)} top-level items")
    for item in program.items:
        if hasattr(item, 'name'):
            print(f"  - {type(item).__name__}: {item.name}")
        else:
            print(f"  - {type(item).__name__}")

def cmd_run(args):
    source = Path(args.file).read_text()
    print(f"=== Running {args.file} (B.E.L. prototype interpreter) ===\n")
    run_bel(source, args.file)

def main():
    parser = argparse.ArgumentParser(
        description="B.E.L. (Better Engineered Language) — Design Validation Prototype",
        epilog="This is a prototype for validating the language design in docs/. The real compiler (belc) is in development."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    p_lex = subparsers.add_parser("lex", help="Tokenize a .bel file")
    p_lex.add_argument("file", help="Path to .bel source file")
    p_lex.set_defaults(func=cmd_lex)
    
    p_parse = subparsers.add_parser("parse", help="Parse a .bel file to AST")
    p_parse.add_argument("file", help="Path to .bel source file")
    p_parse.set_defaults(func=cmd_parse)
    
    p_run = subparsers.add_parser("run", help="Run a .bel file using the prototype interpreter")
    p_run.add_argument("file", help="Path to .bel source file")
    p_run.set_defaults(func=cmd_run)
    
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
