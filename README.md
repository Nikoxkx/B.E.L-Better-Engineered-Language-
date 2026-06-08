# B.E.L. Programming Language

**B.E.L.** — Better Engineered Language

> The systems programming language engineered to finally deliver what developers hoped modern languages would become.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Vision

**B.E.L.** (Better Engineered Language) combines the best ideas from C++, Rust, Go, Zig, Swift, and TypeScript into one coherent, production-grade systems language:

- Rust-level safety with dramatically better ergonomics
- C++-level performance with modern defaults
- Go-level simplicity where it matters
- First-class async, powerful metaprogramming, and predictable costs

## Current Status (Highly Advanced)

**Design Phase: Complete**  
**Prototype Phase: Significantly Expanded**

The project has:
- Complete, cross-referenced design documents for every major subsystem.
- A working, educational prototype that now includes a **borrow checker simulation**.
- Multiple realistic examples demonstrating real language features.
- An active RFC process with initial proposals.
- A realistic skeleton for the future self-hosting `belc` compiler.

**Try it now:**
```bash
python3 prototype/bel_prototype.py run examples/hello.bel
python3 tests/prototype/test_runner.py
```

## Recent Major Additions
- Borrow checker simulation in the prototype
- Structs, enums, traits, generics, Result-based errors, async syntax examples
- Full RFC system started
- Real compiler bootstrap directory (`src/compiler/`)
- Prototype test suite

See [CHANGELOG.md](CHANGELOG.md) for the full list.

## Tooling (Planned Names)
- `belc` — Compiler
- `bel` — Unified CLI + package manager
- `Bel.toml` + `Bel.lock`

## Project Structure

```
bel/
├── README.md
├── docs/                  # Complete language & compiler specifications
├── RFC/                   # Language RFCs (active)
├── examples/              # .bel programs (many now work in prototype)
├── prototype/             # Advanced design-validation prototype (+ borrow checker)
├── src/compiler/          # Future real belc (Rust bootstrap skeleton)
├── stdlib/                # Core + standard library stubs
├── benchmarks/
├── tests/
└── .github/               # GitHub templates
```

## Ready for GitHub & Contribution

This repository is publication-ready:
- Professional documentation
- Clear contribution process
- Issue & PR templates
- Security policy
- Multiple ways to contribute (design, prototype, future compiler, stdlib, docs)

## Next Steps (Community Welcome)

- Expand the prototype further (type checker, more MIR-like features)
- Write more RFCs
- Begin real `belc` implementation in Rust
- Grow the contributor base

Start by reading `docs/vision.md` and trying the prototype.

## License

MIT
