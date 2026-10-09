"""Render layer — markdown + JSON output. The only module allowed to touch disk.

Validators guarantee content quality; this module only formats it, so a
rendering bug can never silently weaken a pass/revise rule.
"""
from __future__ import annotations

import json
from pathlib import Path

from work.fl01_workflow_audit.domain import TargetTask, ToolkitEvidence, WorkflowTask


def render_audit_markdown(
    tasks: tuple[WorkflowTask, ...],
    targets: tuple[TargetTask, ...],
    toolkit: tuple[ToolkitEvidence, ...],
) -> str:
    """Build the 1–2 page workflow audit document."""
    lines = [
        "# FL-01 — Workflow Audit (Setup)",
        "",
        "Internship + study week. Classification follows Mollick's intern frame:",
        "`just me` / `delegate to AI with review` / `collaborate with AI` / `fully automate`.",
        "",
        "## 1. Task table",
        "",
        "| # | Task (real week) | Context | Class | Why |",
        "|---|---|---|---|---|",
    ]
    for task in tasks:
        lines.append(
            f"| {task.id} | {task.title} ({task.weekly_freq}) "
            f"| {task.context} | {task.classification.value} | {task.rationale} |"
        )
    lines += [
        "",
        "## 2. Three target tasks reused in FL-02..FL-04",
        "",
        "| # | Target | Reused in | Done well means |",
        "|---|---|---|---|",
    ]
    for target in targets:
        criteria = "<br>".join(f"{i+1}. {c}" for i, c in enumerate(target.done_well))
        lines.append(f"| {target.id} | {target.title} | {target.reused_in} | {criteria} |")
    lines += [
        "",
        "## 3. Toolkit evidence",
        "",
        "| Tool | Proof | Location | Status |",
        "|---|---|---|---|",
    ]
    for item in toolkit:
        lines.append(
            f"| {item.tool} | {item.kind.value} | `{item.artifact}` | {item.status} |"
        )
    lines += [
        "",
        "> Screenshots: open each tool, capture the account/project screen, and save",
        "> it to the path above. The Claude Project spec is paste-ready in",
        "> `work/fl01_workflow_audit/claude_project_spec.md`.",
        "",
        "## 4. Self-check (mirrors `validators.py`)",
        "",
        f"- {len(tasks)} tasks logged (>={10} required), "
        f"{sum(1 for t in tasks if t.classification.value == 'just me')} marked just-me (>=2 required).",
        "- Every row carries a one-line rationale; every target criterion is measurable.",
        "- Raw queries, client names, and secrets are never pasted into AI tools.",
    ]
    return "\n".join(lines) + "\n"


def build_receipt(
    tasks: tuple[WorkflowTask, ...],
    targets: tuple[TargetTask, ...],
    toolkit: tuple[ToolkitEvidence, ...],
) -> dict:
    """Machine-readable receipt committed alongside the report."""
    return {
        "phase": "FL-01",
        "task_counts": {
            task.classification.value: sum(1 for t in tasks if t.classification is task.classification)
            for task in tasks
        },
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "context": t.context,
                "classification": t.classification.value,
                "rationale": t.rationale,
                "weekly_freq": t.weekly_freq,
            }
            for t in tasks
        ],
        "targets": [
            {"id": g.id, "title": g.title, "reused_in": g.reused_in, "done_well": list(g.done_well)}
            for g in targets
        ],
        "toolkit": [
            {"tool": e.tool, "kind": e.kind.value, "artifact": e.artifact, "status": e.status}
            for e in toolkit
        ],
    }


def write_outputs(markdown: str, receipt: dict, repo_root: Path) -> tuple[Path, Path]:
    """Write the report markdown and JSON receipt; return both paths."""
    md_path = repo_root / "work" / "fl01_workflow_audit.md"
    json_path = repo_root / "work" / "outputs" / "fl01_audit.json"
    md_path.write_text(markdown)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    return md_path, json_path
