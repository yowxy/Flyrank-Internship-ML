"""Audit data — the single source of truth for FL-01 content.

Edit THIS file when the week changes. Validators and renderers consume it;
nothing else duplicates these rows, so the markdown table and the JSON
receipt can never drift apart.

Contexts: "internship" (FlyRank ML track) and "study" (university).
"""
from __future__ import annotations

from work.fl01_workflow_audit.domain import (
    Classification,
    EvidenceKind,
    TargetTask,
    ToolkitEvidence,
    WorkflowTask,
)


def load_tasks() -> tuple[WorkflowTask, ...]:
    """13 recurring tasks from a real internship + study week."""
    return (
        WorkflowTask(
            id="T01",
            title="Derive graded lab-report proofs and statistical arguments",
            context="study",
            classification=Classification.JUST_ME,
            rationale="Graded reasoning must be mine; AI algebra looks plausible while wrong and costs marks.",
            weekly_freq="2x/week",
        ),
        WorkflowTask(
            id="T02",
            title="Final go/no-go on refresh predictions and client-facing wording",
            context="internship",
            classification=Classification.JUST_ME,
            rationale="Accountability and DATA_USE safety cannot be outsourced; I sign every claim.",
            weekly_freq="1x/week",
        ),
        WorkflowTask(
            id="T03",
            title="Boilerplate EDA scaffolding (describe, null-map, dtype table)",
            context="internship",
            classification=Classification.AUTOMATE,
            rationale="Deterministic pandas output; scripted once, re-run on every data drop.",
            weekly_freq="3x/week",
        ),
        WorkflowTask(
            id="T04",
            title="Data-dictionary cross-check of all 44 columns (scale/gotchas)",
            context="internship",
            classification=Classification.DELEGATE_REVIEW,
            rationale="Mechanical comparison AI drafts fast; I verify gotchas like trend leakage.",
            weekly_freq="1x/week",
        ),
        WorkflowTask(
            id="T05",
            title="Warehouse slice aggregation in DuckDB (GROUP BY client/intent)",
            context="internship",
            classification=Classification.DELEGATE_REVIEW,
            rationale="AI drafts SQL fast; I validate row counts and sums before trusting them.",
            weekly_freq="2x/week",
        ),
        WorkflowTask(
            id="T06",
            title="Signal-audit plots plus trend_pct leakage demonstration",
            context="internship",
            classification=Classification.COLLABORATE,
            rationale="I choose hypotheses, AI drafts charts, we iterate on the interpretation.",
            weekly_freq="1x/week",
        ),
        WorkflowTask(
            id="T07",
            title="Hand-rule baseline tuning (copy of 02_baseline_score.py)",
            context="internship",
            classification=Classification.COLLABORATE,
            rationale="Threshold trade-offs need my judgment; AI runs the grid and explains deltas.",
            weekly_freq="1x/week",
        ),
        WorkflowTask(
            id="T08",
            title="Model training harness with client-holdout split (LogReg/RF)",
            context="internship",
            classification=Classification.DELEGATE_REVIEW,
            rationale="Standard sklearn pattern; I check no client appears on both sides of the split.",
            weekly_freq="1x/week",
        ),
        WorkflowTask(
            id="T09",
            title="Related-work literature skim for capstone paper section",
            context="study",
            classification=Classification.DELEGATE_REVIEW,
            rationale="AI summarises fast; I verify every citation exists before it enters the paper.",
            weekly_freq="2x/week",
        ),
        WorkflowTask(
            id="T10",
            title="Colab environment unblock (duckdb install, HF token via getpass)",
            context="internship",
            classification=Classification.COLLABORATE,
            rationale="Pairing unblocks in minutes; I keep secrets out of cells while AI diagnoses.",
            weekly_freq="2x/week",
        ),
        WorkflowTask(
            id="T11",
            title="Commit messages and capstone report copy-editing",
            context="internship",
            classification=Classification.AUTOMATE,
            rationale="Style-only transform; diff-reviewed before anything is committed.",
            weekly_freq="4x/week",
        ),
        WorkflowTask(
            id="T12",
            title="Anki flashcard generation from lecture notes",
            context="study",
            classification=Classification.AUTOMATE,
            rationale="Bulk Q/A transform; I spot-check 10% and delete weak cards weekly.",
            weekly_freq="3x/week",
        ),
        WorkflowTask(
            id="T13",
            title="Weekly timetable planning across internship milestones",
            context="study",
            classification=Classification.DELEGATE_REVIEW,
            rationale="AI proposes the schedule; I enforce real constraints (exams, shift work).",
            weekly_freq="1x/week",
        ),
    )


def load_targets() -> tuple[TargetTask, ...]:
    """Three audit tasks reused in FL-02..FL-04, chained into ML-04/06/07."""
    return (
        TargetTask(
            id="G1",
            title="Data-contract check on the 30k-row starter CSV",
            reused_in="FL-02 / ML-04",
            done_well=(
                "Contract asserts all 44 columns present with documented dtypes.",
                "trend_direction and trend_pct are absent from every feature list.",
                "Run finishes in <60s and writes a committed JSON receipt.",
            ),
        ),
        TargetTask(
            id="G2",
            title="Signal-audit verdict for each candidate feature",
            reused_in="FL-03 / ML-06-07",
            done_well=(
                "Every candidate signal carries a keep/drop verdict with direction.",
                "Each kept signal shows P@50 delta versus the 0.24 hand-rule baseline.",
                "Notebook re-runs top to bottom in <5 minutes with seed 42 and 0 leakage columns.",
            ),
        ),
        TargetTask(
            id="G3",
            title="Ranked refresh queue with reason codes",
            reused_in="FL-04 / ML-07-08",
            done_well=(
                "Queue sorted by score desc; every row carries a human reason code.",
                "Top-50 precision reported under client-holdout split, baseline 0.24 beaten.",
                "Only ~3x lift claimed; no causal language without a design.",
            ),
        ),
    )


def load_toolkit() -> tuple[ToolkitEvidence, ...]:
    """Free-tier toolkit proof pointers (screenshots live next to the report)."""
    return (
        ToolkitEvidence(
            tool="Claude (free)",
            kind=EvidenceKind.SCREENSHOT,
            artifact="work/fl01_workflow_audit/evidence/claude_project.png",
            status="pending-screenshot",
        ),
        ToolkitEvidence(
            tool="ChatGPT (free)",
            kind=EvidenceKind.SCREENSHOT,
            artifact="work/fl01_workflow_audit/evidence/chatgpt_account.png",
            status="pending-screenshot",
        ),
        ToolkitEvidence(
            tool="Anthropic Academy — AI Fluency: Framework & Foundations",
            kind=EvidenceKind.EXPORT,
            artifact="work/fl01_workflow_audit/evidence/academy_module1.png",
            status="pending-screenshot",
        ),
        ToolkitEvidence(
            tool="Claude Project spec (paste-ready custom instructions)",
            kind=EvidenceKind.RECEIPT,
            artifact="work/fl01_workflow_audit/claude_project_spec.md",
            status="configured",
        ),
    )
