# B.E.L. Prototype

Early Python-based prototype of the B.E.L. language frontend and interpreter.

**Purpose:**
- Validate the grammar and design documents in `docs/`
- Provide a runnable environment for early design iteration
- Prove that core language concepts (functions, ownership intuition, control flow, etc.) are sound

**Components**
- `lexer.py` — Hand-written lexer
- `parser.py` — Recursive descent + Pratt parser
- `interpreter.py` — Basic tree-walking interpreter (for validation only)
- `bel_prototype.py` — CLI

**Usage**
```bash
python3 prototype/bel_prototype.py run examples/hello.bel
python3 prototype/bel_prototype.py lex examples/hello.bel
python3 prototype/bel_prototype.py parse examples/hello.bel
```

**Important Limitations**
This is **not** the real compiler or runtime. It has:
- No real type checking or borrow checking
- Simplified semantics
- Only a subset of the planned language
- For design validation and exploration only

The real `belc` compiler will be written in a systems language (with a path to self-hosting in B.E.L.).
