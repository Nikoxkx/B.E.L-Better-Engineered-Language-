# Changelog

## [Unreleased] - 2026-06-08

### Major Progress
- Full rebrand to **B.E.L.** (Better Engineered Language) completed across the entire project.
- All design documents recreated as real files in `docs/`.
- **5 new examples** added: structs/enums, error handling with Result, generics, async syntax, traits.
- **Prototype significantly expanded**:
  - New `borrow_checker.py` module with educational simulation of ownership, moves, shared/mutable borrows.
  - Interpreter now integrates borrow checking and supports structs, assignments, better scoping.
  - Improved error reporting for borrow violations.
- **RFC process launched**:
  - `RFC/0000-template.md`
  - `RFC/0001-simplified-ownership.md`
  - `RFC/0002-first-class-async.md`
- **Real compiler skeleton** created at `src/compiler/` (Rust bootstrap plan documented).
- Added prototype test runner (`tests/prototype/test_runner.py`).
- Basic `stdlib/core/` stub.
- Benchmarks directory with example.
- GitHub-ready enhancements: PR template, FUNDING.yml, improved issue templates.
- All examples now use `.bel` extension.

### Quality Improvements
- Zero references to previous working name.
- Highly consistent branding.
- Professional structure suitable for immediate open-source publication.
