"""Offline contract demonstration; no model, storage or generation occurs."""

import hashlib
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from creation_workbench.contracts import ArtifactRef, RunState, SelectionRef, transition


def main() -> None:
    ref = ArtifactRef("local-workspace", "article-1", "version-1")
    text = "把这一段改短。"
    selected = "这一段"
    selection = SelectionRef(
        ref, "paragraph-2", 1, 4,
        hashlib.sha256(selected.encode("utf-8")).hexdigest(),
    )
    print("Local contract demonstration (no model connected)")
    print("Selection:", selection.validate(ref, "paragraph-2", text))
    state = RunState.CREATED
    for target in (RunState.RUNNING, RunState.WAITING_EXTERNAL, RunState.RUNNING,
                   RunState.NEEDS_REVIEW, RunState.COMPLETED):
        previous, state = state, transition(state, target)
        print(f"{previous.value} -> {state.value}")


if __name__ == "__main__":
    main()
