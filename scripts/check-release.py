#!/usr/bin/env python3
"""Check Git/npm package contents, matching versions, and an optional release tag."""

import json
from pathlib import Path
import re
import subprocess
import sys
import tarfile
import tempfile


root = Path(__file__).resolve().parent.parent
marketplace = json.loads((root / ".agents/plugins/marketplace.json").read_text(encoding="utf-8"))
assert marketplace["name"] == "lesson", "Marketplace must be named lesson"
assert len(marketplace["plugins"]) == 1, "Expected one plugin"
entry = marketplace["plugins"][0]
assert entry["source"]["source"] == "local", "Use the same Git snapshot as the marketplace"
plugin = (root / entry["source"]["path"]).resolve()
assert plugin.is_relative_to(root), "Plugin must stay inside the repository"
manifest = json.loads((plugin / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
assert entry["name"] == manifest["name"] == plugin.name == "lesson", "Plugin names must agree"
assert entry["policy"] == {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL",
}, "Plugin must remain available for installation"

skills = (plugin / manifest["skills"]).resolve()
assert skills.is_relative_to(plugin), "Skills must stay inside the plugin"
assert (skills / "lesson/SKILL.md").is_file(), "Packaged lesson skill is missing"
version = manifest["version"]
package = json.loads((root / "package.json").read_text(encoding="utf-8"))
assert package["version"] == version, "npm and Codex versions must agree"
assert package["pi"]["skills"] == [f"./{skills.relative_to(root).as_posix()}"], "Pi must load the same skills"
assert package["publishConfig"]["access"] == "public", "The npm package must be public"
assert re.fullmatch(r"(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)", version), "Use X.Y.Z"
assert len(sys.argv) <= 2, "Usage: python3 scripts/check-release.py [vX.Y.Z]"
if len(sys.argv) == 2:
    assert sys.argv[1] == f"v{version}", f"Tag {sys.argv[1]} does not match v{version}"

with tempfile.TemporaryDirectory(prefix="lesson-pack-") as temporary:
    packed = subprocess.run(
        ["npm", "pack", "--json", "--ignore-scripts", "--pack-destination", temporary],
        cwd=root, check=True, capture_output=True, text=True,
    )
    archive = Path(temporary) / json.loads(packed.stdout)[0]["filename"]
    with tarfile.open(archive, "r:gz") as bundle:
        required = [
            root / "package.json", root / "README.md", root / "LICENSE",
            plugin / ".codex-plugin/plugin.json", skills / "lesson/SKILL.md",
        ]
        for path in required:
            member = f"package/{path.relative_to(root).as_posix()}"
            assert bundle.extractfile(member).read() == path.read_bytes(), f"npm package differs: {member}"
        assert all(
            member.name in {"package/package.json", "package/README.md", "package/LICENSE"}
            or member.name.startswith("package/plugins/lesson/")
            for member in bundle.getmembers()
        ), "Unexpected files in npm package"
print(f"lesson {version}: Git/npm versions, packaged skill content and tag checks passed")
