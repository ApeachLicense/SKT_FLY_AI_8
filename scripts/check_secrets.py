"""Inspect staged snapshots or all reachable Git history without printing secrets."""
import argparse
import io
from pathlib import Path
import re
import subprocess
import sys
import zipfile

RULES = {
    "azure-storage-key": rb"AccountKey=([A-Za-z0-9+/]{40,}={0,2})",
    "openai-key-or-preview": rb"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{16,}",
    "perplexity-key": rb"\bpplx-[A-Za-z0-9_-]{20,}",
    "tavily-key": rb"\btvly-[A-Za-z0-9_-]{15,}",
    "github-token": rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,})",
    "google-api-key": rb"\bAIza[A-Za-z0-9_-]{30,}",
    "aws-access-key": rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "private-key": rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
    "credential-assignment": rb'''(?im)\b(?:[A-Z_]{0,80}(?:API_KEY|VISION_KEY|ACCESS_TOKEN|AUTH_TOKEN|PASSWORD|SECRET_KEY)|apiKey)["']?\s*[:=]\s*["']([A-Za-z0-9_+/.=-]{20,})["']''',
    "credential-url": rb'''(?i)(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis)://[^\s:'"]+:[^\s@'"]{4,}@''',
}
PATTERNS = {name: re.compile(pattern) for name, pattern in RULES.items()}
PLACEHOLDER = re.compile(rb"(?i)^(?:YOUR_[A-Z_]+|[A-Z_]+_KEY_HERE|[A-Z_]+_TOKEN_HERE|PLACEHOLDER|REDACTED)$")


def find_secrets(data):
    for name, pattern in PATTERNS.items():
        for match in pattern.finditer(data):
            value = match.group(1) if match.lastindex else match.group()
            if PLACEHOLDER.fullmatch(value) or value in (b"x" * len(value), b"0" * len(value)):
                continue
            yield name, data.count(b"\n", 0, match.start()) + 1, value


def inspect(data, label, depth=0):
    if data.startswith(b"PK\x03\x04") or label.lower().endswith(".zip"):
        if depth >= 2:
            raise ValueError("Unpack nested archives before committing source")
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            total = 0
            for entry in archive.infolist():
                if entry.is_dir():
                    continue
                total += entry.file_size
                if entry.file_size > 20_000_000 or total > 100_000_000 or entry.flag_bits & 1:
                    raise ValueError("Archive cannot be fully inspected; commit unpacked source instead")
                yield from inspect(archive.read(entry), label + "!" + entry.filename, depth + 1)
        return
    # Known key signatures are checked in binary blobs as well as text.
    for name, line, _ in find_secrets(data):
        yield label, name, line


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.PIPE)


def objects(repo, history):
    if not history:
        for entry in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
            if entry:
                info, path = entry.split(b"\t", 1)
                yield info.split()[1], path.decode("utf-8", errors="replace")
        return
    mapping = {}
    for line in git(repo, "rev-list", "--objects", "--all").splitlines():
        sha, separator, path = line.partition(b" ")
        if separator:
            mapping[sha] = path.decode("utf-8", errors="replace")
    checked = subprocess.run(["git", "-C", str(repo), "cat-file", "--batch-check=%(objectname) %(objecttype)"], input=b"\n".join(mapping) + b"\n", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    for line in checked.stdout.splitlines():
        sha, kind = line.split()
        if kind == b"blob":
            yield sha, mapping[sha]


def scan(repo, history):
    issues, count = set(), 0
    process = subprocess.Popen(["git", "-C", str(repo), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for sha, path in objects(repo, history):
            process.stdin.write(sha + b"\n")
            process.stdin.flush()
            header = process.stdout.readline().split()
            if len(header) != 3 or header[0] != sha or header[1] != b"blob":
                raise ValueError("Cannot inspect a Git blob")
            data = process.stdout.read(int(header[2]))
            if len(data) != int(header[2]) or process.stdout.read(1) != b"\n":
                raise ValueError("Incomplete Git blob")
            issues.update(inspect(data, path))
            count += 1
        process.stdin.close()
        if process.wait() != 0:
            raise ValueError("Git object reader failed")
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
    if history:
        messages = git(repo, "log", "--all", "--format=%B", "-z")
        issues.update(inspect(messages, "commit messages"))
    return sorted(issues), count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--staged", action="store_true")
    modes.add_argument("--history", action="store_true")
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        issues, count = scan(args.repo, args.history)
    except (ValueError, zipfile.BadZipFile, RuntimeError, subprocess.SubprocessError, OSError) as exc:
        print("Secret scan could not complete; commit/push blocked (" + type(exc).__name__ + ").", file=sys.stderr)
        return 2
    for path, rule, line in issues:
        print(f"{path}:{line}: {rule}", file=sys.stderr)
    if issues:
        print(f"Blocked: {len(issues)} credential locations found. Values are hidden.", file=sys.stderr)
        return 1
    print(f"Secret scan passed: {count} Git blobs inspected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
