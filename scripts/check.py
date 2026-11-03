"""Run bootstrap checks without external dependencies; preserve a fresh receipt."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def input_hashes() -> dict[str, str]:
    paths = [p for p in ROOT.iterdir() if p.is_file()]
    for folder in ("src", "scripts", "tests", "examples", "docs", "references",
                   "infrastructure", ".github", "web"):
        paths.extend(p for p in (ROOT / folder).rglob("*")
                     if p.is_file() and not set(p.relative_to(ROOT).parts).intersection(
                         {"node_modules", "dist", "__pycache__"}
                     ) and not any(part.endswith(".egg-info") for part in p.parts)
                     and p.suffix not in {".pyc", ".tsbuildinfo"})
    return {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--with-api", action="store_true")
    args = parser.parse_args()
    out = args.out.resolve()
    try:
        out.relative_to(ROOT)
    except ValueError:
        parser.error("--out must be inside this repository (prefer test-runs/<name>)")
    # Avoid output becoming an input, and never overwrite a failed receipt.
    if (ROOT / "test-runs") not in out.parents:
        parser.error("--out must be a new directory under test-runs/")
    out.mkdir(parents=True, exist_ok=False)
    before = input_hashes()
    env = dict(os.environ, PYTHONPATH=str(ROOT / "src"), PYTHONUTF8="1")
    steps = [
        ("bootstrap", [sys.executable, "scripts/validate_bootstrap.py"]),
        ("contracts", [sys.executable, "-m", "unittest", "discover", "-s", "tests",
                       "-p", "test_*.py", "-v"]),
        ("example", [sys.executable, "examples/local_contracts.py"]),
    ]
    if args.with_api:
        steps.append(("api", [sys.executable, "-m", "unittest", "discover",
                              "-s", "tests/api", "-p", "test_*.py", "-v"]))
    records = []
    for name, command in steps:
        started = time.monotonic()
        try:
            result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=120)
            code, stdout, stderr = result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired as exc:
            code, stdout, stderr = 124, exc.stdout or b"", (exc.stderr or b"") + b"\nTimed out"
        except OSError as exc:
            code, stdout, stderr = 127, b"", str(exc).encode("utf-8")
        (out / f"{name}.stdout.log").write_bytes(stdout)
        (out / f"{name}.stderr.log").write_bytes(stderr)
        records.append({"name": name, "command": command, "exitCode": code,
                        "seconds": round(time.monotonic() - started, 3),
                        "stdout": f"{name}.stdout.log", "stderr": f"{name}.stderr.log"})
        print(f"{name}: {'PASS' if code == 0 else 'FAIL'}", flush=True)
        if code:
            print(stderr.decode("utf-8", errors="replace")[-4000:])
    after = input_hashes()
    passed = bool(records) and all(r["exitCode"] == 0 for r in records) and before == after
    git = shutil.which("git")
    head = subprocess.run([git, "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                          text=True, timeout=15).stdout.strip() if git else None
    report = {
        "schema": "creation-workbench-check/v1",
        "status": "BOOTSTRAP_CHECKS_PASS" if passed else "FAIL",
        "passed": passed, "timestamp": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "executable": sys.executable, "gitHead": head,
        "projectRoot": str(ROOT), "commands": records,
        "inputFilesSha256": before, "inputsUnchanged": before == after,
        "changedDuringExecution": sorted(k for k in before.keys() | after.keys()
                                         if before.get(k) != after.get(k)),
        "notRun": ["real_model", "persistence", "worker_recovery", "web_build", "installed_wheel"]
                  + ([] if args.with_api else ["api"]),
        "g0Accepted": False,
        "limitation": "Bootstrap checks only; no real model, SDK, storage or product acceptance.",
    }
    (out / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                                     encoding="utf-8")
    print(report["status"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
