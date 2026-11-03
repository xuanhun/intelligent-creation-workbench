"""Run using an isolated Python with only the built core wheel installed."""

from importlib.metadata import distribution
from pathlib import Path
import sys

import creation_workbench
from creation_workbench.contracts import InvalidTransition, RunState, transition


def main() -> None:
    package_path = Path(creation_workbench.__file__).resolve()
    assert package_path.is_relative_to(Path(sys.prefix).resolve()), package_path
    assert "site-packages" in package_path.parts, package_path
    installed = distribution("intelligent-creation-workbench")
    assert creation_workbench.__version__ == installed.version == "0.0.1a0"
    assert installed.read_text("direct_url.json") is not None
    assert transition(RunState.CREATED, RunState.RUNNING) == RunState.RUNNING
    try:
        transition(RunState.CANCELLED, RunState.RUNNING)
    except InvalidTransition:
        pass
    else:
        raise AssertionError("Cancelled run was resurrected")
    assert package_path.with_name("py.typed").is_file()
    print(f"Installed core wheel verified: {package_path}")


if __name__ == "__main__":
    main()
