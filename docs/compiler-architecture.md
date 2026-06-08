# B.E.L. Compiler Architecture

**Version:** 0.1.0  
**Date:** 2026-06-08  
**Status:** Draft

## High-Level Pipeline
```
Source (.bel)
  ↓ Lexer
  ↓ Parser → AST
  ↓ Semantic Analysis + Macro Expansion
  ↓ Type Checker → HIR
  ↓ Borrow Checker
  ↓ MIR (SSA)
  ↓ Optimizations (const folding, inlining, escape analysis, ...)
  ↓ Code Generation → LLVM IR
  ↓ LLVM Optimizations + Codegen
  ↓ Machine Code / WASM / Object Files
```

## Frontend
- Hand-written or generated lexer with excellent source locations.
- Recursive descent + Pratt parser.
- Hygienic declarative + procedural macros (expand before semantic analysis).
- Name resolution, type checking (Hindley-Milner + trait solver).
- HIR (typed, desugared).
- Borrow checker with Non-Lexical Lifetimes.

## Mid & Backend
- MIR for optimization and drop elaboration.
- LLVM as primary backend (mature targets: x86_64, aarch64, riscv, wasm32, etc.).
- Future: Cranelift or custom backends.
- Full debug info, LTO, PGO support.

## Key Features
- Incremental compilation (fingerprinting).
- Powerful `const fn` evaluation.
- World-class diagnostics with suggestions.
- Cross-compilation via target triples.
- Designed for self-hosting after stabilization.

## Bootstrapping
Phase 1: Written in host language (Rust/C++).  
Phase 2: Self-hosting B.E.L. compiler.

Security: Sandboxed procedural macros, careful untrusted input handling.
