"""Composition root — validate, then render. The only place with side effects.

Usage:
    python -m work.fl01_workflow_audit.run_audit [--check-only]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from work.fl01_workflow_audit.audit_data import load_targets, load_tasks, load_toolkit
from work.fl01_workflow_audit.render import build_receipt, render_audit_markdown, write_outputs
from work.fl01_workflow_audit.validators import validate_targets, validate_tasks


def main(check_only: bool = False) -> int:
    tasks, targets, toolkit = load_tasks(), load_targets(), load_toolkit()
    violations = validate_tasks(tasks) + validate_targets(targets)
    if violations:
        print("FL-01 FAIL:")
        for violation in violations:
            print(f"  - {violation}")
        return 1
    print(f"FL-01 PASS: {len(tasks)} tasks, {len(targets)} targets, {len(toolkit)} toolkit items.")
    if not check_only:
        md_path, json_path = write_outputs(
            render_audit_markdown(tasks, targets, toolkit),
            build_receipt(tasks, targets, toolkit),
            REPO_ROOT,
        )
        print(f"wrote {md_path.relative_to(REPO_ROOT)}")
        print(f"wrote {json_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate and render the FL-01 audit.")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    raise SystemExit(main(check_only=args.check_only))
