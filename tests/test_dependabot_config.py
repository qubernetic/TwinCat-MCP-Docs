"""Rules of the Dependabot config, .github/dependabot.yml.

Dependabot's pull requests run the build job with the Dependabot secret
BRAND_DEPLOY_KEY, so the config pins what may be updated and where the pull
requests go.
"""

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / ".github" / "dependabot.yml"


def load_config():
    return yaml.safe_load(CONFIG.read_text(encoding="utf-8"))


def updates_by_ecosystem():
    return {u["package-ecosystem"]: u for u in load_config()["updates"]}


def test_updates_actions_and_pip_only():
    # The brand submodule moves by hand, when the theme's mkdocs/ changes.
    assert load_config()["version"] == 2
    assert sorted(updates_by_ecosystem()) == ["github-actions", "pip"]


def test_pip_covers_both_requirement_files():
    pip = updates_by_ecosystem()["pip"]
    assert sorted(pip.get("directories", [])) == ["/", "/tests"]
    assert "directory" not in pip


def test_material_moves_only_with_the_brand_pin():
    ignored = [i["dependency-name"] for i in updates_by_ecosystem()["pip"].get("ignore", [])]
    assert ignored == ["mkdocs-material"]


def test_pull_requests_go_to_develop_weekly_and_grouped():
    for name, update in updates_by_ecosystem().items():
        assert update.get("target-branch") == "develop", name
        assert update.get("schedule", {}).get("interval") == "weekly", name
        groups = update.get("groups", {})
        assert len(groups) == 1, name
        (group,) = groups.values()
        assert group.get("patterns") == ["*"], name
