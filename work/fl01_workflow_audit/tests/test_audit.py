"""Contract tests for FL-01 — one test per pass/revise criterion.

Run: python -m unittest discover -s work.fl01_workflow_audit.tests -v
"""
from __future__ import annotations

import unittest

from work.fl01_workflow_audit.audit_data import load_targets, load_tasks, load_toolkit
from work.fl01_workflow_audit.domain import Classification
from work.fl01_workflow_audit.validators import validate_targets, validate_tasks


class TestAuditContract(unittest.TestCase):
    def test_tasks_pass(self):
        tasks = load_tasks()
        self.assertEqual(validate_tasks(tasks), [])
        self.assertGreaterEqual(len(tasks), 10)

    def test_two_just_me_with_reasons(self):
        just_me = [t for t in load_tasks() if t.classification is Classification.JUST_ME]
        self.assertGreaterEqual(len(just_me), 2)
        for task in just_me:
            self.assertGreaterEqual(len(task.rationale.split()), 6)

    def test_every_task_classified_with_rationale(self):
        for task in load_tasks():
            self.assertIsInstance(task.classification, Classification)
            self.assertTrue(task.title.strip())
            self.assertTrue(task.rationale.strip())

    def test_targets_measurable(self):
        targets = load_targets()
        self.assertEqual(validate_targets(targets), [])
        self.assertEqual(len(targets), 3)

    def test_toolkit_covers_required_tools(self):
        names = " ".join(e.tool for e in load_toolkit()).lower()
        for required in ("claude", "chatgpt", "academy"):
            self.assertIn(required, names)


if __name__ == "__main__":
    unittest.main()
