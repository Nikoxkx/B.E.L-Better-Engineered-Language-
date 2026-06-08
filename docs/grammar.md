# B.E.L. Grammar Definition

**Version:** 0.1.0  
**Date:** 2026-06-08  
**Status:** Draft

This document defines the formal grammar of B.E.L. using extended EBNF.

## Lexical Grammar
Identifiers, integers (with bases and suffixes), floats, strings, chars, keywords (see language-spec.md), operators, and punctuation are defined.

## Program Structure
```
program ::= item*
item    ::= visibility? (function | struct | enum | trait | impl | mod | use | const | static | ...)
```

## Key Productions
- Functions with `async? fn name(params) -> type? { body }`
- Types: primitives, references `&mut? T`, arrays `[T; N]`, slices `[T]`, tuples, paths with generics.
- Expressions with full precedence for binary ops, control flow expressions, calls, field access, etc.
- Patterns for match and let.

Full details are implemented and validated in the `prototype/` parser.

See the prototype for a working recursive descent + Pratt parser matching this grammar.
