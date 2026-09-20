#!/usr/bin/env python3
"""Validate the Lab 01 roster.

Two students may share a status code - the code is derived from the GitHub
handle and is checked here, not reserved.

Run it yourself before you open a pull request - it is exactly the same script
that CI runs, so if it passes here it will pass there:

    python3 tools/validate_roster.py

To also check that your pull request only touches your own file (this is what
CI does on a PR):

    python3 tools/validate_roster.py --base origin/main
"""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from http import HTTPStatus
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "server"))
from status_codes import CLAIMABLE_CODES, PREFERRED_LANGUAGES  # noqa: E402


def expected_code(github_handle: str) -> int:
    """Same mapping as /slot in server/main.py."""
    digest = hashlib.sha256(github_handle.strip().lower().encode()).hexdigest()
    return CLAIMABLE_CODES[int(digest, 16) % len(CLAIMABLE_CODES)]


ROSTER_DIR = Path(__file__).resolve().parent.parent / "roster"
REQUIRED_KEYS = {"github_handle", "http_code", "description", "preferred_language", "encrypted_alias"}
HANDLE_RE = re.compile(r"^[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}$")
MIN_DESCRIPTION_CHARS = 40
RSA_2048_CIPHERTEXT_BYTES = 256


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def error(self, path: Path | str, message: str) -> None:
        self.errors.append(f"{path}: {message}")

    def note(self, message: str) -> None:
        self.notes.append(message)


def roster_files(roster_dir: Path) -> list[Path]:
    """Every roster entry, ignoring the worked example."""
    return sorted(p for p in roster_dir.glob("*.json") if not p.name.startswith("_"))


def validate_entry(path: Path, report: Report) -> dict | None:
    try:
        raw = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        report.error(path.name, "file is not valid UTF-8")
        return None

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        report.error(path.name, f"not valid JSON - {exc.msg} at line {exc.lineno}, column {exc.colno}")
        return None

    if not isinstance(data, dict):
        report.error(path.name, "top level must be a JSON object, not a list or a bare value")
        return None

    missing = REQUIRED_KEYS - data.keys()
    if missing:
        report.error(path.name, f"missing required field(s): {', '.join(sorted(missing))}")
    unexpected = data.keys() - REQUIRED_KEYS
    if unexpected:
        report.error(path.name, f"unexpected field(s): {', '.join(sorted(unexpected))}")
    if missing:
        return None

    handle = data["github_handle"]
    if not isinstance(handle, str) or not HANDLE_RE.match(handle):
        report.error(path.name, f"github_handle {handle!r} is not a valid lowercase GitHub username")
    elif path.stem != handle:
        report.error(path.name, f"filename must match github_handle - rename the file to {handle}.json")

    code = data["http_code"]
    if not isinstance(code, int) or isinstance(code, bool):
        report.error(path.name, f"http_code must be a number, not {type(code).__name__}")
    elif code not in CLAIMABLE_CODES:
        report.error(path.name, f"http_code {code} is not one of the codes used in Lab 01")
    elif isinstance(handle, str) and code != expected_code(handle):
        report.error(
            path.name,
            f"http_code {code} is not the code /slot gives for '{handle}' - "
            "run curl \"http://localhost:8000/slot?github_handle=<handle>\" again",
        )

    description = data["description"]
    if not isinstance(description, str):
        report.error(path.name, "description must be a string")
    else:
        stripped = description.strip()
        if len(stripped) < MIN_DESCRIPTION_CHARS:
            report.error(
                path.name,
                f"description is {len(stripped)} characters, at least {MIN_DESCRIPTION_CHARS} are required - "
                "explain when a server would send this code and why",
            )
        elif isinstance(code, int) and code in CLAIMABLE_CODES:
            canonical = HTTPStatus(code).phrase.lower()
            if stripped.lower() in {canonical, f"{code} {canonical}"}:
                report.error(path.name, "description is just the status code's official name - write your own explanation")

    language = data["preferred_language"]
    if language == "php":
        report.error(path.name, "PHP is explicitly excluded by the semester project assignment. Pick something else.")
    elif language not in PREFERRED_LANGUAGES:
        report.error(
            path.name,
            f"preferred_language {language!r} must be one of: {', '.join(PREFERRED_LANGUAGES)}",
        )

    alias = data["encrypted_alias"]
    if not isinstance(alias, str):
        report.error(path.name, "encrypted_alias must be a base64 string")
    else:
        try:
            decoded = base64.b64decode(alias, validate=True)
        except (binascii.Error, ValueError):
            report.error(path.name, "encrypted_alias is not valid base64 - re-run tools/encrypt_me.sh")
        else:
            if len(decoded) != RSA_2048_CIPHERTEXT_BYTES:
                report.error(
                    path.name,
                    f"encrypted_alias decodes to {len(decoded)} bytes, expected {RSA_2048_CIPHERTEXT_BYTES} "
                    "for an RSA-2048 ciphertext - did you paste your plaintext alias by mistake?",
                )

    return data


def check_pr_scope(base: str, report: Report) -> None:
    """On a pull request, you add exactly one file: your own roster entry."""
    try:
        diff = subprocess.run(
            ["git", "diff", "--name-status", f"{base}...HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout
    except subprocess.CalledProcessError as exc:
        report.note(f"could not diff against {base}, skipping scope check ({exc})")
        return

    added, touched = [], []
    for line in diff.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status, path = parts[0], parts[-1]
        if status.startswith("A"):
            added.append(path)
        else:
            touched.append(f"{status} {path}")

    roster_prefix = "lab01-onboarding/roster/"
    non_roster = [p for p in added if not p.startswith(roster_prefix)]

    if touched:
        report.errors.append(
            "this pull request modifies or deletes files that are not yours: "
            + ", ".join(touched)
            + ". Lab 01 pull requests only ADD one new file."
        )
    if non_roster:
        report.errors.append(
            "this pull request adds files outside the roster directory: " + ", ".join(non_roster)
        )
    roster_added = [p for p in added if p.startswith(roster_prefix)]
    if len(roster_added) > 1:
        report.errors.append(
            "this pull request adds more than one roster file: " + ", ".join(roster_added)
        )
    elif not roster_added and not touched and not non_roster:
        report.errors.append("this pull request does not add a roster file - nothing to review")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", help="git ref to diff against, e.g. origin/main (enables the PR scope check)")
    parser.add_argument("--roster", type=Path, default=ROSTER_DIR, help="roster directory to check")
    args = parser.parse_args()

    report = Report()
    files = roster_files(args.roster)

    entries: dict[Path, dict] = {}
    for path in files:
        data = validate_entry(path, report)
        if data is not None:
            entries[path] = data

    if args.base:
        check_pr_scope(args.base, report)

    print(f"Checked {len(files)} roster entr{'y' if len(files) == 1 else 'ies'}.")
    for note in report.notes:
        print(f"  note: {note}")

    if report.errors:
        print(f"\n{len(report.errors)} problem(s) found:\n")
        for err in report.errors:
            print(f"  - {err}")
        print("\nFix these and push again. The same script runs in CI.")
        return 1

    print("All good.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
