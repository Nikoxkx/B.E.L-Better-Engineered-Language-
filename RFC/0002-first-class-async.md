# RFC 0002: First-Class Async/Await

**Status:** Draft  
**Author:** B.E.L. Design Team  
**Date:** 2026-06-08

## Summary

Make `async fn` and `await` first-class language features with excellent ergonomics and a high-performance default executor.

## Motivation

Async is critical for modern systems (networking, I/O, GUIs). Many languages have painful async stories (Rust's borrow checker pain with futures, Go's goroutines with GC).

## Guide-level Explanation

```bel
async fn fetch(url: &str) -> Result<string, Error> { ... }

async fn main() {
    let data = await fetch("https://example.com");
    println("Got: {}", data);
}
```

## Key Design Points

- `async fn` returns a `Future`.
- `await` is an expression.
- Structured concurrency primitives in std.
- Work-stealing executor provided by default.
- Excellent integration with the ownership model (reduced pain compared to early Rust).

See `docs/runtime-architecture.md` for details.

## Drawbacks

- Still requires understanding of futures in advanced cases.
- Executor choice matters for some domains.

## Prior Art

Rust (lessons learned), Swift (structured concurrency), Kotlin coroutines.

## Unresolved Questions

- Exact cancellation model.
- How to best support custom executors.
