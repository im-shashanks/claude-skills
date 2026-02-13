#!/usr/bin/env python3
"""Check for Shaktra plugin updates by comparing local and remote versions."""

import json
import subprocess
import sys
from pathlib import Path


def read_local_version(plugin_root: str) -> tuple[str, str]:
    """Return (version, repository_url) from local plugin.json."""
    plugin_json = Path(plugin_root) / ".claude-plugin" / "plugin.json"
    if not plugin_json.exists():
        return "", ""
    data = json.loads(plugin_json.read_text())
    return data.get("version", ""), data.get("repository", "")


def parse_github_owner_repo(url: str) -> tuple[str, str]:
    """Extract owner and repo from a GitHub URL."""
    # Handle https://github.com/owner/repo or https://github.com/owner/repo.git
    url = url.rstrip("/").removesuffix(".git")
    parts = url.split("/")
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    return "", ""


def fetch_remote_version(owner: str, repo: str) -> str:
    """Fetch remote plugin version from GitHub. Returns version string or empty."""
    raw_url = (
        f"https://raw.githubusercontent.com/{owner}/{repo}"
        f"/main/dist/shaktra/.claude-plugin/plugin.json"
    )
    try:
        result = subprocess.run(
            ["curl", "-sf", "--max-time", "5", raw_url],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            data = json.loads(result.stdout)
            return data.get("version", "")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
        pass

    # Fallback: gh CLI
    try:
        result = subprocess.run(
            ["gh", "api",
             f"repos/{owner}/{repo}/contents/dist/shaktra/.claude-plugin/plugin.json",
             "--jq", ".content"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0 and result.stdout.strip():
            import base64
            decoded = base64.b64decode(result.stdout.strip()).decode()
            data = json.loads(decoded)
            return data.get("version", "")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, OSError):
        pass

    return ""


def compare_semver(local: str, remote: str) -> str:
    """Compare semver strings. Returns 'up_to_date', 'update_available', or 'ahead'."""
    try:
        l_parts = [int(x) for x in local.split(".")]
        r_parts = [int(x) for x in remote.split(".")]
        for l, r in zip(l_parts, r_parts):
            if r > l:
                return "update_available"
            if l > r:
                return "ahead"
        return "up_to_date"
    except (ValueError, AttributeError):
        return "up_to_date"


def main():
    if len(sys.argv) < 2:
        print("Usage: check_version.py <plugin_root>", file=sys.stderr)
        sys.exit(1)

    plugin_root = sys.argv[1]
    local_version, repo_url = read_local_version(plugin_root)

    if not local_version:
        print(json.dumps({"error": "plugin.json not found"}))
        sys.exit(0)

    result = {
        "local_version": local_version,
        "repository": repo_url,
    }

    if not repo_url:
        result["status"] = "no_repository"
        print(json.dumps(result))
        sys.exit(0)

    owner, repo = parse_github_owner_repo(repo_url)
    if not owner or not repo:
        result["status"] = "invalid_repository"
        print(json.dumps(result))
        sys.exit(0)

    remote_version = fetch_remote_version(owner, repo)
    if not remote_version:
        result["status"] = "offline"
        print(json.dumps(result))
        sys.exit(0)

    result["remote_version"] = remote_version
    result["status"] = compare_semver(local_version, remote_version)
    print(json.dumps(result))


if __name__ == "__main__":
    main()
