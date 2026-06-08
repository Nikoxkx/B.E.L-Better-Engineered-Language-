# B.E.L. Compiler (`belc`)

This directory will contain the real B.E.L. compiler.

## Bootstrapping Plan

1. **Initial implementation** (2027): Written in Rust (or C++) for rapid development and to leverage LLVM.
2. **Self-hosting** (late 2028 / 2029): The compiler will be rewritten in B.E.L. itself.

## Current Structure (Stub)

- `frontend/` — Lexer, Parser, Semantic Analysis, Type Checker, Borrow Checker
- `ir/` — HIR and MIR definitions + transformations
- `backend/` — LLVM IR generation + future alternative backends
- `driver/` — Main entry point, CLI handling, session management

See `docs/compiler-architecture.md` for the full pipeline design.

## How to Build (Future)

Once the Rust bootstrap exists:
```bash
cargo build --release
./target/release/belc --help
```

For now, the Python prototype in `prototype/` is the best way to experiment with the language.
