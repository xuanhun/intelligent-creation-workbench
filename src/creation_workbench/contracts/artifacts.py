"""Immutable references and a minimal text-selection conflict guard."""

from dataclasses import dataclass
import hashlib
import re


class SelectionConflict(ValueError):
    """The selected content no longer matches the requested base."""


@dataclass(frozen=True)
class ArtifactRef:
    workspace_id: str
    artifact_id: str
    version_id: str

    def __post_init__(self) -> None:
        for name in ("workspace_id", "artifact_id", "version_id"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a nonempty string")


@dataclass(frozen=True)
class SelectionRef:
    """Offsets use Python Unicode code points, end exclusive.

    This is an internal contract. Web editors using UTF-16 offsets must
    explicitly convert them before constructing this reference.
    """

    artifact: ArtifactRef
    object_id: str
    start: int
    end: int
    original_sha256: str

    def __post_init__(self) -> None:
        if not isinstance(self.artifact, ArtifactRef):
            raise ValueError("artifact must be an ArtifactRef")
        if not isinstance(self.object_id, str) or not self.object_id.strip():
            raise ValueError("object_id is required")
        if type(self.start) is not int or type(self.end) is not int:
            raise ValueError("selection offsets must be integers")
        if self.start < 0 or self.end <= self.start:
            raise ValueError("selection must be a nonempty half-open range")
        if not isinstance(self.original_sha256, str) or not re.fullmatch(
            r"[0-9a-f]{64}", self.original_sha256
        ):
            raise ValueError("original_sha256 must be a lowercase SHA256 digest")

    def validate(self, current: ArtifactRef, object_id: str, text: str) -> str:
        """Return matching selected text or reject a stale/mismatched target.

        Authorization and atomic version commits are separate service checks.
        """
        if current != self.artifact or object_id != self.object_id:
            raise SelectionConflict("artifact, workspace, version or object changed")
        if self.end > len(text):
            raise SelectionConflict("selection exceeds current object")
        selected = text[self.start:self.end]
        if hashlib.sha256(selected.encode("utf-8")).hexdigest() != self.original_sha256:
            raise SelectionConflict("selected text changed")
        return selected
