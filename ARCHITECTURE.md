# B.E.L. Architecture Overview

High-level view of the B.E.L. ecosystem.

## Layers
Applications & Libraries (B.E.L.)
  ↑
Standard Library
  ↑
Runtime (memory, async, threading, panic handling)
  ↑
Compiler (belc)
  ↑
LLVM / Alternative Backends
  ↑
OS / Bare Metal / WASM

## Major Subsystems
- Language Core (defined in docs/)
- Compiler (src/compiler) — see docs/compiler-architecture.md
- Runtime — see docs/runtime-architecture.md
- Toolchain — see docs/toolchain.md
- Package Ecosystem — see docs/package-ecosystem.md

Key IRs: Tokens → AST → HIR → MIR → LLVM IR.

## Extensibility
Custom allocators, executors, macros, build scripts, LSP extensions, future backends.

## Evolution
Designed for 10+ years of growth and self-hosting.
