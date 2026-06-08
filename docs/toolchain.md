# B.E.L. Toolchain Design

**Version:** 0.1.0  
**Date:** 2026-06-08  
**Status:** Draft

## Core Tools
- `belc` — Compiler driver (incremental, parallel, rich diagnostics, cross-compilation, `--emit` options).
- `bel` — Unified CLI (`bel new`, `bel build`, `bel run`, `bel test`, `bel fmt`, `bel lint`, `bel doc`, `bel pkg`...).
- Package manager (`bel pkg`) with modern features.
- Formatter, linter, test runner, docs generator.
- Full Language Server (`bel-lsp`) with autocomplete, go-to-def, rename, hover, diagnostics, code actions, semantic tokens.

## Manifest
`Bel.toml` (package metadata, dependencies, profiles, targets).

## Performance Goals
- `bel check` on small project: < 100ms
- Fast incremental builds
- Excellent IDE experience

## Extensibility
Build scripts, procedural macros, custom lints, LSP extensions.
