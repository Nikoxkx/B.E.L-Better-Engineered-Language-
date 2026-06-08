# RFC 0001: Simplified Ownership Model

**Status:** Draft  
**Author:** B.E.L. Design Team  
**Date:** 2026-06-08

## Summary

Adopt a Rust-inspired ownership system with aggressive lifetime elision, default Copy for small types, and first-class support for regions/arenas to reduce friction while preserving safety.

## Motivation

Rust's ownership model is powerful but has a steep learning curve. Many developers are scared away by lifetimes and borrow checker errors. B.E.L. aims to keep the safety guarantees while making the common case much easier.

## Guide-level Explanation

- Variables own their data by default.
- `let x = y` moves (or copies if small/Copy).
- `&x` creates a shared borrow.
- `&mut x` creates an exclusive borrow.
- Most lifetimes are inferred.
- Small values (i32, small structs) copy automatically.

## Reference-level Explanation

See `docs/ownership-model.md` for the detailed rules.

Key simplifications:
1. Aggressive elision (often zero annotations needed).
2. Copy by default for types without heap allocation or interior mutability.
3. Explicit `Region` and `Arena` types for temporary high-performance allocation.

## Drawbacks

- Slightly less fine-grained control than full Rust in some edge cases.
- May require `Rc`/`Arc` more often for complex graphs.

## Rationale and Alternatives

We considered full Rust model, Go GC, and Zig manual management. This is the best balance of safety + ergonomics.

## Prior Art

Rust (core ideas), Swift (ARC + ownership experiments), Zig (manual with safety tools).

## Unresolved Questions

- Exact rules for auto-Copy on user types.
- How regions interact with async.

## Future Possibilities

Linear types for resources, effect systems.
