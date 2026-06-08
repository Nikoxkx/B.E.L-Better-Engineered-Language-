# B.E.L. — Better Engineered Language

**B.E.L.** (Better Engineered Language) is a next-generation systems programming language designed to combine the best ideas from modern systems and application languages without their compromises. (And also it's just cool lol.)

It targets **Rust-level safety**, **C++-level performance**, **Go-level simplicity in the common case**, **Zig-level transparency**, and **Swift/Kotlin-level ergonomics**.

> The systems programming language that developers hoped modern languages would eventually become.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-Design%20Complete%20%7C%20Advanced%20Prototype-blue)](docs/multi-year-roadmap.md)

---

## Table of Contents

- [Why B.E.L.?](#why-bel)
- [Current Status](#current-status)
- [Try It Now](#try-it-now)
- [Key Language Features](#key-language-features)
- [Documentation](#documentation)
- [Examples](#examples)
- [Roadmap](#roadmap)
- [Project Structure](#project-structure)
- [Tooling & Ecosystem](#tooling--ecosystem)
- [Contributing](#contributing)
- [License](#license)

---

## Why B.E.L.?

Most modern systems languages force painful trade-offs:

| Language | Strengths                        | Weaknesses                          | B.E.L. Approach                     |
|----------|----------------------------------|-------------------------------------|-------------------------------------|
| **Rust** | Memory safety                    | Steep learning curve, complex async | Same safety, much simpler model     |
| **C++**  | Performance + ecosystem          | Memory safety issues                | Modern safety without losing speed  |
| **Go**   | Simplicity + concurrency         | Limited control, GC overhead        | Zero-cost abstractions + control    |
| **Zig**  | Transparency + simplicity        | No safety guarantees                | Full safety with transparency       |
| **Swift**| Ergonomics                       | Limited systems-level control       | Full systems power + ergonomics     |

**B.E.L.** is built on the principle that you should not have to choose between **safety**, **performance**, **simplicity**, and **control**.

---

## Current Status

**Phase 0: Design Complete** (2026)  
**Phase 1: Advanced Prototype & Early Implementation**

### What Exists Today

- ✅ Complete, production-grade language design (all major subsystems specified)
- ✅ Advanced Python prototype with **borrow checker simulation**
- ✅ 10+ realistic examples
- ✅ Active RFC process
- ✅ Full compiler architecture stub for the future `belc`
- ✅ Comprehensive documentation

The project follows a strict **"design first"** philosophy — all foundational specifications were completed before significant implementation began.

---

## Try It Now

The prototype lets you explore the language syntax and semantics today.

```bash
# Run an example
python3 prototype/bel_prototype.py run examples/hello.bel

# Run the prototype test suite
python3 tests/prototype/test_runner.py

# Explore the language
python3 prototype/bel_prototype.py lex examples/hello.bel
python3 prototype/bel_prototype.py parse examples/structs_and_enums.bel
```

The prototype now includes an educational **borrow checker** that enforces core ownership rules and reports violations.

---

## Key Language Features

### Memory Safety
- Ownership + Borrowing (inspired by Rust but significantly simplified)
- First-class Regions and Arenas
- No garbage collection by default
- Optional `Rc` / `Arc` for shared ownership

### Modern Language Features
- First-class `async` / `await`
- Powerful pattern matching
- Generics with const generics
- Traits (interfaces) with default methods
- `Result<T, E>` error handling with `?` operator
- No exceptions

### Performance & Control
- Zero-cost abstractions
- Compile-time evaluation (`constexpr`)
- Safe, debuggable metaprogramming
- Explicit control over memory and performance
- Predictable costs — no hidden allocations

### Ergonomics
- Strong type inference
- Minimal lifetime annotations in common cases
- Excellent, actionable error messages (goal)

---

## Documentation

All design documents are complete and cross-referenced.

### Core Language
- [Vision & Philosophy](docs/vision.md)
- [Formal Language Specification](docs/language-spec.md)
- [Grammar Definition](docs/grammar.md)
- [Type System](docs/type-system.md)
- [Ownership & Borrowing Model](docs/ownership-model.md)

### Compiler & Runtime
- [Compiler Architecture](docs/compiler-architecture.md)
- [Runtime Architecture](docs/runtime-architecture.md)

### Tooling & Ecosystem
- [Toolchain Design](docs/toolchain.md)
- [Package Ecosystem](docs/package-ecosystem.md)

### Planning
- [Multi-Year Roadmap](docs/multi-year-roadmap.md)
- [Architecture Overview](ARCHITECTURE.md)

---

## Examples

The `examples/` directory contains realistic programs written in B.E.L.

### Currently Runnable in Prototype
| File                        | Description                              |
|----------------------------|------------------------------------------|
| `hello.bel`                | Classic Hello World + functions          |
| `simple_demo.bel`          | Basic variables, arithmetic, loops       |
| `ownership_demo.bel`       | Move semantics and borrowing intuition   |
| `async_demo.bel`           | Async/await syntax demonstration         |

### Language Showcase (Design Demonstrations)
| File                          | Features Demonstrated                     |
|------------------------------|-------------------------------------------|
| `structs_and_enums.bel`      | Structs, enums, pattern matching          |
| `error_handling.bel`         | `Result<T,E>` and error handling          |
| `generics.bel`               | Generic types                             |
| `traits.bel`                 | Traits / Interfaces                       |
| `borrow_violation_demo.bel`  | Code that triggers the borrow checker     |
| `fibonacci.bel`              | Recursion and iteration                   |

Run any example with:
```bash
python3 prototype/bel_prototype.py run examples/<name>.bel
```

---

## Roadmap

See the full plan in [docs/multi-year-roadmap.md](docs/multi-year-roadmap.md).

### High-Level Timeline

| Phase       | Period     | Goals                                      | Status      |
|-------------|------------|--------------------------------------------|-------------|
| **0**       | 2026       | Complete design + advanced prototype       | ✅ Done     |
| **1**       | 2027       | Bootstrap compiler (`belc`) + core language| In planning |
| **2**       | 2027–2028  | Tooling, stdlib, async, package manager    | Future      |
| **3**       | 2028–2029  | Performance, WebAssembly, self-hosting     | Future      |
| **4**       | 2029       | 1.0 Stabilization                          | Future      |
| **5+**      | 2030+      | Advanced features, ecosystem growth        | Future      |

---

## Project Structure

```
bel/
├── README.md
├── Bel.toml                     # Package manifest (future)
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
├── ROADMAP.md
├── ARCHITECTURE.md
│
├── docs/                        # Complete language & compiler specifications
│   ├── vision.md
│   ├── language-spec.md
│   ├── grammar.md
│   ├── type-system.md
│   ├── ownership-model.md
│   ├── compiler-architecture.md
│   ├── runtime-architecture.md
│   ├── toolchain.md
│   ├── package-ecosystem.md
│   └── multi-year-roadmap.md
│
├── RFC/                         # Request for Comments (language design)
│   ├── 0000-template.md
│   ├── 0001-simplified-ownership.md
│   └── 0002-first-class-async.md
│
├── examples/                    # B.E.L. source code examples
│
├── prototype/                   # Advanced design validation prototype
│   ├── bel_prototype.py         # Main CLI
│   ├── lexer.py
│   ├── parser.py
│   ├── interpreter.py
│   ├── borrow_checker.py        # Educational ownership simulation
│   └── README.md
│
├── src/compiler/                # Future real compiler (belc)
│   └── (Rust bootstrap skeleton)
│
├── stdlib/                      # Standard library (early stubs)
│
├── tests/                       # Test infrastructure
│   └── prototype/
│
├── benchmarks/                  # Performance benchmarks (stubs)
│
└── .github/                     # GitHub templates and configuration
```

---

## Tooling & Ecosystem (Planned)

| Tool              | Purpose                              | Command          |
|-------------------|--------------------------------------|------------------|
| **belc**          | The compiler                         | `belc main.bel`  |
| **bel**           | Unified CLI                          | `bel build`, `bel test` |
| **bel pkg**       | Package manager                      | `bel pkg add`    |
| **bel fmt**       | Code formatter                       | `bel fmt`        |
| **bel lint**      | Linter                               | `bel lint`       |
| **Language Server** | IDE support (autocomplete, etc.)   | -                |

Manifest format: `Bel.toml` + `Bel.lock`

---

## Contributing

We are actively looking for contributors in the following areas:

- Language design & writing RFCs
- Improving the prototype (parser, borrow checker, interpreter)
- Documentation and examples
- Standard library design
- Future compiler implementation

**Getting started:**
1. Read [docs/vision.md](docs/vision.md)
2. Explore the prototype and examples
3. Look at open RFCs in the `RFC/` directory
4. See [CONTRIBUTING.md](CONTRIBUTING.md)

All contributions are welcome — from design discussions to code.

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

**B.E.L.** — Better Engineered Language.  
Designed with rigor. Built for the long term. and just cause its cool lol
