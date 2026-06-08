# B.E.L. Type System Specification

**Version:** 0.1.0  
**Date:** 2026-06-08  
**Status:** Draft

## Overview
B.E.L. features a strong, static, nominal type system with powerful inference, generics, traits, and algebraic data types. It is sound, expressive, ergonomic, and predictable.

## Primitive Types
`i8`..`i128`, `isize`, `u8`..`u128`, `usize`, `f32`, `f64`, `bool`, `char`, `string`, `()`.

## Composite Types
- Arrays `[T; N]`
- Slices `[T]`
- Tuples `(T1, T2)`
- Structs (nominal)
- Enums (sum types with data-carrying variants)
- References `&T` / `&mut T`
- Raw pointers (unsafe only)

## Generics & Traits
```bel
struct Vector<T> { ... }

trait Add<Rhs = Self> {
    type Output;
    fn add(self, rhs: Rhs) -> Self::Output;
}
```

## Inference
Strong local inference. Public APIs usually require annotations.

## Special Types
- `Option<T>`, `Result<T,E>` (library but with language support for `?` and patterns)
- Never type `!`
- Const generics

## Lifetimes
Part of the type system (see ownership-model.md).

The type system + ownership system together guarantee absence of entire classes of memory safety bugs in safe code.
