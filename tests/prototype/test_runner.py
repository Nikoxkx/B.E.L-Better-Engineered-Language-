#!/usr/bin/env python3
"""
B.E.L. Prototype Test Runner

Tests examples that are currently supported by the prototype parser.
More advanced examples in examples/ demonstrate intended language features
from the design documents.
"""

import subprocess
import sys
from pathlib import Path

# Curated list of examples the current prototype can reliably parse & run
WORKING_EXAMPLES = [
    "examples/hello.bel",
    "examples/simple_demo.bel",
    "examples/ownership_demo.bel",
    "examples/async_demo.bel",
]

def run_test(example: str) -> bool:
    print(f"Testing {example}...", end=" ")
    try:
        result = subprocess.run(
            [sys.executable, "prototype/bel_prototype.py", "run", example],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print("OK")
            return True
        else:
            print("FAILED")
            if result.stderr:
                print("  " + result.stderr.strip()[:200])
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("=== B.E.L. Prototype Test Suite ===\n")
    passed = 0
    for ex in WORKING_EXAMPLES:
        if run_test(ex):
            passed += 1
    print(f"\n{passed}/{len(WORKING_EXAMPLES)} tests passed.")
    print("\nNote: Other .bel files in examples/ show intended syntax from the language spec.")
    print("They will become runnable as the prototype parser is improved.")
