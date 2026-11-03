from dataclasses import FrozenInstanceError
import hashlib
import unittest

from creation_workbench.contracts import (
    ArtifactRef, InvalidTransition, RunState, SelectionConflict, SelectionRef, transition,
)


class RunTests(unittest.TestCase):
    def test_wait_resume_review_complete(self):
        state = RunState.CREATED
        for target in (RunState.RUNNING, RunState.WAITING_EXTERNAL, RunState.RUNNING,
                       RunState.NEEDS_REVIEW, RunState.RUNNING, RunState.NEEDS_REVIEW,
                       RunState.COMPLETED):
            state = transition(state, target)
        self.assertEqual(state, RunState.COMPLETED)

    def test_cancellation_at_each_active_stage(self):
        for state in (RunState.CREATED, RunState.RUNNING, RunState.WAITING_EXTERNAL,
                      RunState.NEEDS_REVIEW):
            self.assertEqual(transition(state, RunState.CANCELLED), RunState.CANCELLED)

    def test_terminal_states_cannot_be_resurrected(self):
        for state in (RunState.COMPLETED, RunState.FAILED, RunState.CANCELLED):
            for target in RunState:
                with self.subTest(state=state, target=target), self.assertRaises(InvalidTransition):
                    transition(state, target)

    def test_execution_cannot_skip_review(self):
        for state in (RunState.CREATED, RunState.RUNNING, RunState.WAITING_EXTERNAL):
            with self.assertRaises(InvalidTransition):
                transition(state, RunState.COMPLETED)


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.ref = ArtifactRef("workspace-a", "article-a", "v1")
        self.text = "甲😀乙段落"
        self.selection = SelectionRef(
            self.ref, "paragraph-1", 1, 3,
            hashlib.sha256("😀乙".encode("utf-8")).hexdigest(),
        )

    def test_unicode_and_unchanged_target(self):
        self.assertEqual(self.selection.validate(self.ref, "paragraph-1", self.text), "😀乙")

    def test_wrong_workspace_artifact_version_or_object_is_rejected(self):
        for current in (ArtifactRef("workspace-b", "article-a", "v1"),
                        ArtifactRef("workspace-a", "article-b", "v1"),
                        ArtifactRef("workspace-a", "article-a", "v2")):
            with self.assertRaises(SelectionConflict):
                self.selection.validate(current, "paragraph-1", self.text)
        with self.assertRaises(SelectionConflict):
            self.selection.validate(self.ref, "paragraph-2", self.text)

    def test_changed_or_shortened_text_is_rejected(self):
        for text in ("甲😀丙段落", "甲"):
            with self.assertRaises(SelectionConflict):
                self.selection.validate(self.ref, "paragraph-1", text)

    def test_references_are_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            self.ref.version_id = "v2"

    def test_invalid_offsets_hash_and_identifiers(self):
        for start, end in ((-1, 2), (2, 2), (3, 1), (True, 2), (0, 1.5)):
            with self.assertRaises(ValueError):
                SelectionRef(self.ref, "p1", start, end, "a" * 64)
        with self.assertRaises(ValueError):
            SelectionRef(self.ref, "p1", 0, 1, "bad-hash")
        with self.assertRaises(ValueError):
            ArtifactRef(" ", "a", "v1")


if __name__ == "__main__":
    unittest.main()
