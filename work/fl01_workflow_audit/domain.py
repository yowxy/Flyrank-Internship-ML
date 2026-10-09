"""Domain layer — pure types, zero I/O, zero dependencies.

Clean-architecture role: enterprise entities. Everything here is a frozen
dataclass or Enum so audit objects are hashable, comparable, and trivially
serialisable. No file, network, or datetime-now access allowed in this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Classification(str, Enum):
    """Mollick-task routing decision for one recurring task."""

    JUST_ME = "just me"
    DELEGATE_REVIEW = "delegate to AI with review"
    COLLABORATE = "collaborate with AI"
    AUTOMATE = "fully automate"


class EvidenceKind(str, Enum):
    SCREENSHOT = "screenshot"
    EXPORT = "export"
    RECEIPT = "receipt"


@dataclass(frozen=True)
class WorkflowTask:
    """One recurring task from the intern's real week."""

    id: str  # stable key, e.g. "T04"
    title: str
    context: str  # "internship" | "study"
    classification: Classification
    rationale: str  # exactly one line of reasoning
    weekly_freq: str  # e.g. "3x/week"


@dataclass(frozen=True)
class TargetTask:
    """One of the three audit tasks reused in FL-02..FL-04."""

    id: str  # e.g. "G1"
    title: str
    reused_in: str  # e.g. "FL-02 / ML-04"
    done_well: tuple[str, ...]  # measurable acceptance criteria


@dataclass(frozen=True)
class ToolkitEvidence:
    """Proof that a required free-tier tool account exists."""

    tool: str
    kind: EvidenceKind
    artifact: str  # path or description of the proof, never a secret
    status: str  # "configured" | "pending-screenshot"
