"""Validators — pure functions; no I/O, no exceptions for control flow.

Each rule maps 1:1 to a pass/revise criterion from the assignment card, so a
failing suite message tells the intern exactly what to fix.
"""
from __future__ import annotations

from work.fl01_workflow_audit.domain import Classification, TargetTask, WorkflowTask

MIN_TASKS = 10
MIN_JUST_ME = 2
FORBIDDEN_TOKENS = ("TODO", "TBD", "lorem", "xxx")


def validate_tasks(tasks: tuple[WorkflowTask, ...]) -> list[str]:
    """Return a list of violations; empty means the audit table passes."""
    violations: list[str] = []
    if len(tasks) < MIN_TASKS:
        violations.append(f"need >={MIN_TASKS} tasks, found {len(tasks)}")
    seen_ids = [t.id for t in tasks]
    if len(set(seen_ids)) != len(seen_ids):
        violations.append("task ids must be unique")
    just_me = [t for t in tasks if t.classification is Classification.JUST_ME]
    if len(just_me) < MIN_JUST_ME:
        violations.append(f"need >={MIN_JUST_ME} 'just me' tasks, found {len(just_me)}")
    for task in tasks:
        if not task.title.strip() or not task.rationale.strip():
            violations.append(f"{task.id}: title and rationale must be non-empty")
        if len(task.rationale.split()) < 6:
            violations.append(f"{task.id}: rationale is not one substantive line")
        lowered = (task.title + " " + task.rationale).lower()
        if any(tok in lowered for tok in FORBIDDEN_TOKENS):
            violations.append(f"{task.id}: placeholder text detected")
    return violations


def _has_number(text: str) -> bool:
    return any(ch.isdigit() for ch in text)


def validate_targets(targets: tuple[TargetTask, ...]) -> list[str]:
    """Three specific targets, each with measurable success definitions.

    Measurable = verifiable by re-running an artifact: a numeric threshold
    (preferred) or a binary assertion an auditor can check mechanically
    (e.g. "asserts", "absent", "sorted", "committed", "verdict", "reason").
    Each target must carry >=2 numeric criteria so success is never vibes-only.
    """
    verifiable_tokens = (
        "assert", "absent", "present", "sorted", "committed",
        "verdict", "reason", "seed", "re-run", "rerun", "top to bottom",
    )
    violations: list[str] = []
    if len(targets) != 3:
        violations.append(f"need exactly 3 target tasks, found {len(targets)}")
    for target in targets:
        if len(target.done_well) < 2:
            violations.append(f"{target.id}: needs >=2 success criteria")
        numeric = 0
        for criterion in target.done_well:
            words = criterion.split()
            if len(words) < 5:
                violations.append(f"{target.id}: criterion too vague: {criterion!r}")
            lowered = criterion.lower()
            checkable = _has_number(criterion) or any(
                tok in lowered for tok in verifiable_tokens
            )
            if not checkable:
                violations.append(
                    f"{target.id}: criterion not verifiable: {criterion!r}"
                )
            if _has_number(criterion):
                numeric += 1
        if len(target.done_well) >= 2 and numeric < 2:
            violations.append(f"{target.id}: needs >=2 numeric criteria, found {numeric}")
    return violations
