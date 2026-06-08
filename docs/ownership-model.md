# B.E.L. Ownership Model

**Version:** 0.1.0  
**Date:** 2026-06-08  
**Status:** Draft

## Philosophy
B.E.L. adopts an ownership-based memory management model inspired by Rust but deliberately simplified for better ergonomics while retaining strong safety guarantees.

## Core Rules
1. Every value has exactly one owner.
2. Ownership can be moved.
3. When the owner goes out of scope, the value is dropped.
4. Borrowing: `&T` (shared) or `&mut T` (exclusive).
5. The borrow checker enforces: one mutable OR many shared borrows at a time. Borrows cannot outlive the owner.

## Simplifications vs Rust
- More aggressive lifetime elision (often completely inferred).
- Non-lexical lifetimes from day one.
- Small types (primitives, small structs) are `Copy` by default.
- First-class regions and arenas for high-performance temporary allocation.
- `Rc<T>` / `Arc<T>` available when true shared ownership is needed.

## Advanced Features
- Explicit arenas/regions for batch allocation and collective freeing.
- Custom allocators.
- Clear `unsafe` escape hatch with responsibility on the programmer.

See the compiler architecture for how the borrow checker is integrated into the pipeline.
