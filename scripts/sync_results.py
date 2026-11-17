#!/usr/bin/env python3
"""Copy the result tables and figures this paper uses from dx300-sim into results/.

Run from the repository root:

    python3 scripts/sync_results.py            # or: make sync
    python3 scripts/sync_results.py --src /path/to/dx300-sim --dest /tmp/out

The dx300-sim checkout is only read, never written. Files that do not exist yet
are skipped with a warning. results/SOURCE.md records the dx300-sim commit hash
and, per file, whether the copy matched that commit.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SRC = Path(os.environ.get("DX300_SIM", "~/ahmed/dx300-sim")).expanduser()
DEFAULT_DEST = REPO_ROOT / "results"
SIM_URL = "https://github.com/Ahmedayyadw/dx300-sim"

# Paths relative to the dx300-sim root. An entry may be a glob pattern.
# Files are copied flat into results/, so basenames must be unique.
SOURCES = [
    "rl/12e_stats.md",
    "rl/12g_sensitivity.md",
    "rl/12f_loads.md",
    "rl/11_real_plant_tuning.md",
    "rl/13_benchmark.md",  # Lab 13: benchmark tables and their reading
    "rl/13_benchmark.csv",  # Lab 13: the same rows at full precision
    "paper/figs/lab13/*.pdf",  # Lab 13: Fig. 1 to Fig. 5
    "paper/figs/lab13/README.md",  # Lab 13: source and limits of every figure
    "rl/12_eval.csv",  # Lab 12: per-row results; energy floor and fast PID point
    "rl/boom_env_real_robust.py",  # training env of every learner; the reward
    "rl/14_reward_fix.md",  # Lab 14: corrected reward, reward-hacking check, BC
    "rl/14_benchmark.csv",  # Lab 14: the benchmark rows at full precision
    "rl/13e_direction_split.md",  # Lab 13e: boom-up / boom-down split of E_mech
]


def warn(msg: str) -> None:
    print(f"WARNING: {msg}", file=sys.stderr)


def git(src: Path, *args: str) -> str:
    """Run a read-only git command in src. --no-optional-locks keeps git from
    refreshing the index there, so nothing in dx300-sim is written."""
    out = subprocess.run(
        ["git", "--no-optional-locks", "-C", str(src), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return out.stdout.strip()


def state_at_sync(src: Path, rel: str) -> str:
    """Say whether the file on disk is the one in the recorded commit."""
    code = git(src, "status", "--porcelain", "--ignored", "--", rel)[:2]
    if not code:
        return "matches commit"
    if code in ("??", "!!"):
        return "NOT in commit (untracked)"
    return "DIFFERS from commit (uncommitted changes)"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy result tables and figures from dx300-sim into results/.")
    parser.add_argument("--src", type=Path, default=DEFAULT_SRC,
                        help=f"dx300-sim checkout (default: {DEFAULT_SRC})")
    parser.add_argument("--dest", type=Path, default=DEFAULT_DEST,
                        help=f"output directory (default: {DEFAULT_DEST})")
    args = parser.parse_args()
    src = args.src.expanduser().resolve()
    dest = args.dest.expanduser().resolve()

    if not (src / ".git").exists():
        print(f"ERROR: {src} is not a git checkout of dx300-sim", file=sys.stderr)
        return 1
    if dest == src or src in dest.parents:
        print(f"ERROR: --dest {dest} is inside dx300-sim; refusing to write there",
              file=sys.stderr)
        return 1

    commit = git(src, "rev-parse", "HEAD")
    commit_date = git(src, "show", "-s", "--format=%cI", "HEAD")
    branch = git(src, "rev-parse", "--abbrev-ref", "HEAD")

    dest.mkdir(parents=True, exist_ok=True)
    rows: list[tuple[str, str, str, str]] = []
    missing: list[str] = []
    seen: dict[str, str] = {}

    for pattern in SOURCES:
        matches = sorted(p for p in src.glob(pattern) if p.is_file())
        if not matches:
            warn(f"missing in dx300-sim, skipped: {pattern}")
            missing.append(pattern)
            continue
        for path in matches:
            rel = path.relative_to(src).as_posix()
            if path.name in seen:
                print(f"ERROR: {rel} and {seen[path.name]} have the same file name",
                      file=sys.stderr)
                return 1
            seen[path.name] = rel
            shutil.copy2(path, dest / path.name)
            state = state_at_sync(src, rel)
            rows.append((path.name, rel, state, sha256(path)[:12]))
            print(f"copied  {rel} -> {dest / path.name}")
            if state != "matches commit":
                warn(f"{rel}: {state}")

    lines = [
        "# Result sources",
        "",
        "Written by `scripts/sync_results.py`. Do not edit by hand. Change the files",
        "in dx300-sim, then run `make sync`.",
        "",
        f"- Source repository: {SIM_URL}",
        f"- Commit: [`{commit}`]({SIM_URL}/commit/{commit})",
        f"- Commit date: {commit_date}",
        f"- Branch: `{branch}`",
        "",
        "| File | Source path | State at sync | SHA-256 (first 12) |",
        "|------|-------------|---------------|--------------------|",
    ]
    lines += [f"| `{n}` | `{r}` | {s} | `{h}` |" for n, r, s, h in rows]
    if missing:
        lines += ["", "## Missing at sync", ""]
        lines += [f"- `{m}`" for m in missing]
    (dest / "SOURCE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"wrote   {dest / 'SOURCE.md'} (dx300-sim commit {commit[:7]})")
    print(f"done: {len(rows)} copied, {len(missing)} missing")
    return 0


if __name__ == "__main__":
    sys.exit(main())
