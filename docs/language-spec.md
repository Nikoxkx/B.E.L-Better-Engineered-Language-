# B.E.L. Formal Language Specification

**Version:** 0.1.0  
**Date:** 2026-06-08  
**Status:** Draft

## 1. Introduction

This document provides the formal specification for the B.E.L. programming language. B.E.L. is a statically typed, compiled, systems programming language with strong emphasis on memory safety, performance, and developer ergonomics.

## 2. Lexical Structure

Source files are UTF-8. 

**Keywords** include: `fn`, `let`, `const`, `struct`, `enum`, `trait`, `impl`, `match`, `if`, `else`, `loop`, `while`, `for`, `in`, `break`, `continue`, `return`, `async`, `await`, `unsafe`, `pub`, `mut`, `mod`, `use`, `import`, `where`, `type`, `static`, `extern`, `constexpr`, `macro`, etc.

**Literals**: integers (with `i32`/`u64` suffixes, hex/binary/octal), floats, strings (including raw), chars, booleans.

## 3. Core Constructs

### Modules
```bel
mod math;
import std::collections::HashMap;
use std::io::{self, Read};
```

### Functions
```bel
fn add(a: i32, b: i32) -> i32 { a + b }

async fn fetch(url: &str) -> Result<String, Error> { ... }
```

### Variables & Constants
```bel
let x = 42;
let mut y: u64 = 100;
const PI: f64 = 3.14159;
```

### Structs, Enums, Traits
```bel
struct Point { x: f64, y: f64 }

enum Result<T, E> { Ok(T), Err(E) }

trait Drawable {
    fn draw(&self);
}
```

## 4. Expressions & Control Flow

Full support for `if`/`else`, `match` (exhaustive), `loop`/`while`/`for`, pattern matching, `?` operator for `Result`/`Option`.

## 5. Ownership & Borrowing

See dedicated [ownership-model.md](ownership-model.md).

## 6. Type System

See [type-system.md](type-system.md).

## 7. Error Handling
No exceptions. Use `Result<T, E>` + `?` operator.

## 8. Concurrency
`spawn`, channels, `async`/`await`, structured concurrency.

## 9. Memory Model
Stack by default. Heap via `Box`/`Vec`. First-class arenas and regions. Optional `Rc`/`Arc`.

## 10. Interoperability
C FFI via `extern "C"`. Future C++ and WASM support.

This is a living document. Major changes go through the RFC process.
