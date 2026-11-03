"""Validate source syntax, design provenance and local documentation links."""

import ast
import hashlib
import json
from pathlib import Path
import re
import tomllib

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["name"] == "intelligent-creation-workbench"
    assert project["project"]["dependencies"] == [], "Core must remain dependency-free"
    for folder in ("src", "scripts", "tests", "examples"):
        for path in (ROOT / folder).rglob("*.py"):
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    plan = json.loads((ROOT / "docs/iteration-plan.json").read_text(encoding="utf-8"))
    rows = {row["id"]: row for row in plan["iterations"]}
    assert len(rows) == len(plan["iterations"])
    assert plan["nextIteration"] in rows
    for row in rows.values():
        assert row["status"] in {"complete", "planned", "in_progress", "blocked"}
        assert all(dep in rows for dep in row["dependsOn"])
        if row["status"] == "complete":
            assert row["evidence"], "Complete iterations require evidence"
            assert all(rows[dep]["status"] == "complete" for dep in row["dependsOn"])
            for evidence in row["evidence"]:
                assert (ROOT / evidence).is_file(), evidence
    sources = json.loads((ROOT / "references/sources.json").read_text(encoding="utf-8"))
    for source in sources["snapshots"]:
        path = ROOT / source["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"], str(path)
    for path in [*ROOT.glob("*.md"), *ROOT.glob("docs/**/*.md"),
                 ROOT / "references/README.md", ROOT / "infrastructure/README.md"]:
        for link in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" in link or link.startswith("#"):
                continue
            target = link.split("#", 1)[0]
            assert (path.parent / target).exists(), f"Broken link: {path}: {target}"
    print("Bootstrap syntax, plan, provenance and documentation links verified")


if __name__ == "__main__":
    main()
