"""Rules of the docs workflow, .github/workflows/deploy-docs.yml.

The build job holds the read-only deploy key of the private brand repository,
so these tests pin who can run it, where the key may appear, and how the site
is installed, built and published. They are ported from copia-cli's
test/workflows/docs_test.go, which guards the same shape there.
"""

import re
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = ROOT / ".github" / "workflows" / "deploy-docs.yml"

# The condition that limits a job or step of the workflow to main.
MAIN_REF = "github.ref == 'refs/heads/main'"
# The condition that keeps the build, and with it the deploy key, off pull
# requests from forks, which get no secrets.
SAME_REPO = (
    "github.event_name != 'pull_request' || "
    "github.event.pull_request.head.repo.full_name == github.repository"
)
# The secrets context as a word, so secrets.X, secrets['X'] and
# toJSON(secrets) all count.
SECRETS_RE = re.compile(r"\bsecrets\b")
USES_RE = re.compile(r"^\s*(-\s*)?uses:")
PINNED_USES_RE = re.compile(
    r"^\s*(-\s*)?uses:\s*[\w.-]+/[\w./-]+@[0-9a-f]{40} # v\d+(\.\d+)*\s*$"
)


def raw_workflow():
    return WORKFLOW.read_text(encoding="utf-8")


def load_workflow():
    wf = yaml.safe_load(raw_workflow())
    # PyYAML reads the bare key `on` as the boolean True.
    if True in wf:
        wf["on"] = wf.pop(True)
    return wf


def text(value):
    """Render a YAML value as the workflow file spells it."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value)


def steps_of(wf, job):
    return wf["jobs"].get(job, {}).get("steps", [])


def uses_action(step, action):
    return text(step.get("uses")).lower().startswith(action + "@")


def without_comments(raw):
    """Drop the comment lines of a workflow, which run nothing."""
    return "\n".join(
        line for line in raw.split("\n") if not line.strip().startswith("#")
    )


def pip_installs(raw):
    """Every line of a workflow that runs pip install, trimmed."""
    return [
        line.strip()
        for line in raw.split("\n")
        if "pip install" in line or "pip3 install" in line
    ]


def requirements_file(line):
    """The file a `pip3 install --require-hashes -r <file>` line installs.

    Returns (file, problem); problem is empty when the line is acceptable.
    """
    fields = line.split()
    i = 0
    while i < len(fields) and fields[i] != "install":
        i += 1
    file = ""
    hashes = False
    i += 1
    while i < len(fields):
        field = fields[i]
        if field == "--require-hashes":
            hashes = True
        elif field == "-r" and i + 1 < len(fields):
            i += 1
            file = fields[i]
        elif field.startswith("-"):
            pass
        else:
            return "", (
                f"{line!r} names the package {field}; install it from a "
                "requirements file with hashes"
            )
        i += 1
    if not file or not hashes:
        return "", f"{line!r} does not install with --require-hashes -r <file>"
    return file, ""


def unhashed_requirements(data):
    """Every requirement not pinned with == or without a --hash=sha256: entry."""
    bad = []
    for req in data.replace("\\\n", " ").split("\n"):
        i = req.find("#")
        if i >= 0 and "--hash" not in req[:i]:
            req = req[:i]
        req = req.strip()
        if not req:
            continue
        name = req.split()[0]
        if "==" not in name or "--hash=sha256:" not in req:
            bad.append(name)
    return bad


def test_triggers():
    wf = load_workflow()
    assert sorted(wf["on"]) == ["pull_request", "push", "workflow_dispatch"]
    assert wf["on"]["push"]["branches"] == ["main"]
    assert "pull_request_target" not in raw_workflow()


def test_build_skips_fork_pull_requests():
    wf = load_workflow()
    assert wf["jobs"]["build"].get("if") == SAME_REPO
    for name in ("rules", "deploy"):
        assert "pull_request" not in text(wf["jobs"][name].get("if")), name


def test_deploys_from_main_only():
    wf = load_workflow()
    deploy = wf["jobs"].get("deploy")
    assert deploy is not None, "no deploy job"
    assert deploy.get("if") == MAIN_REF
    assert sorted(deploy.get("needs") or []) == ["build", "rules"]
    pages_uploads = rehearsals = 0
    for name in ("build", "deploy"):
        for i, step in enumerate(steps_of(wf, name), 1):
            where = f"job {name} step {i}"
            if uses_action(step, "actions/upload-pages-artifact"):
                pages_uploads += 1
                assert name == "build" and step.get("if") == MAIN_REF, where
            elif uses_action(step, "actions/upload-artifact"):
                rehearsals += 1
                assert step.get("if") == "github.ref != 'refs/heads/main'", where
            elif uses_action(step, "actions/deploy-pages"):
                assert name == "deploy", where
    assert (pages_uploads, rehearsals) == (1, 1)
    for name in wf["jobs"]:
        if name in ("build", "deploy"):
            continue
        for i, step in enumerate(steps_of(wf, name), 1):
            assert not uses_action(step, "actions/upload-pages-artifact"), (name, i)
            assert not uses_action(step, "actions/deploy-pages"), (name, i)


def test_brand_key_stays_in_one_step():
    wf = load_workflow()
    raw = raw_workflow()
    assert len(SECRETS_RE.findall(without_comments(raw))) == 1
    for name, job in wf["jobs"].items():
        assert not SECRETS_RE.search(text(job.get("env"))), name
        if name != "build":
            assert not SECRETS_RE.search(str(job)), name
    steps = steps_of(wf, "build")
    keyed = [
        i
        for i, s in enumerate(steps)
        if SECRETS_RE.search(
            " ".join(text(s.get(k)) for k in ("with", "env", "run", "if"))
        )
    ]
    assert len(keyed) == 1, f"build steps {keyed} reference the secrets context"
    brand = steps[keyed[0]]
    assert uses_action(brand, "actions/checkout")
    want = {
        "repository": "qubernetic/brand",
        "path": "brand",
        "persist-credentials": "false",
        "ref": "${{ steps.brand.outputs.sha }}",
        "ssh-key": "${{ secrets.BRAND_DEPLOY_KEY }}",
    }
    for key, value in want.items():
        assert text(brand.get("with", {}).get(key)) == value, key
    pins = [i for i, s in enumerate(steps) if s.get("id") == "brand"]
    assert pins and pins[0] < keyed[0], "no step with id brand before the brand checkout"
    # The pin is read in an assignment of its own, so a failed git rev-parse
    # fails the step under bash -e instead of passing an empty ref, which
    # would check out the brand's default branch.
    pin_lines = text(steps[pins[0]].get("run")).strip().split("\n")
    assert [l.strip() for l in pin_lines] == [
        "sha=$(git rev-parse HEAD:brand)",
        'echo "sha=$sha" >> "$GITHUB_OUTPUT"',
    ]
    checkouts = [i for i, s in enumerate(steps) if uses_action(s, "actions/checkout")]
    assert len(checkouts) == 2
    assert checkouts[0] != keyed[0], "build has no checkout of its own before the brand"
    own = steps[checkouts[0]].get("with", {})
    assert text(own.get("persist-credentials")) == "false"
    assert "ssh-key" not in own
    assert "submodules" not in own


def test_first_checkout_fetches_full_history():
    # git-revision-date-localized dates every page today on a shallow clone.
    wf = load_workflow()
    first = next(s for s in steps_of(wf, "build") if uses_action(s, "actions/checkout"))
    assert text(first.get("with", {}).get("fetch-depth")) == "0"


def test_build_is_strict():
    wf = load_workflow()
    build = wf["jobs"]["build"]
    assert "continue-on-error" not in build
    found = 0
    for i, step in enumerate(build["steps"], 1):
        assert "continue-on-error" not in step, f"build step {i}"
        run = text(step.get("run")).strip()
        if "mkdocs build --strict" not in run:
            continue
        found += 1
        assert not any(c in run for c in "|;&\n"), f"build step {i} runs {run!r}"
    assert found == 1


def test_rehearsal_cannot_cancel_a_deploy():
    wf = load_workflow()
    concurrency = wf.get("concurrency")
    group = concurrency.get("group") if isinstance(concurrency, dict) else concurrency
    assert group == "pages-${{ github.ref }}"
    # A second run on main (a dispatch or a push) must not cancel a deploy
    # that is publishing the live site; other refs may cancel their own runs.
    assert concurrency.get("cancel-in-progress") == "${{ github.ref != 'refs/heads/main' }}"


def test_permissions_are_least():
    wf = load_workflow()
    assert wf.get("permissions") == {"contents": "read"}
    for name, job in wf["jobs"].items():
        if name == "deploy":
            assert job.get("permissions") == {"pages": "write", "id-token": "write"}
        else:
            assert "permissions" not in job, name


def test_actions_are_pinned_by_sha():
    lines = [l for l in raw_workflow().split("\n") if USES_RE.match(l)]
    assert lines
    for line in lines:
        assert PINNED_USES_RE.match(line), line


def test_runners_are_pinned():
    wf = load_workflow()
    for name, job in wf["jobs"].items():
        assert job.get("runs-on") == "ubuntu-24.04", name


def test_scripts_have_no_expressions():
    wf = load_workflow()
    for name in wf["jobs"]:
        for i, step in enumerate(steps_of(wf, name), 1):
            assert "${{" not in text(step.get("run")), f"job {name} step {i}"


def test_installs_are_hashed():
    lines = pip_installs(raw_workflow())
    # rules installs the test tools, build the site's lock; nothing else.
    assert [requirements_file(l)[0] for l in lines] == [
        "tests/requirements.txt",
        "requirements.txt",
    ]
    for line in lines:
        assert re.fullmatch(r"(-\s*)?(run:\s*)?pip3 install --require-hashes -r \S+", line), line
        file, problem = requirements_file(line)
        assert not problem, problem
        path = ROOT / file
        assert path.is_file(), file
        assert unhashed_requirements(path.read_text(encoding="utf-8")) == [], file


@pytest.mark.parametrize(
    "line, file",
    [
        ("pip3 install --require-hashes -r rpmbuild/requirements.txt", "rpmbuild/requirements.txt"),
        ("pip3 install --require-hashes --no-build-isolation -r a.txt", "a.txt"),
        ("pip install -r a.txt --require-hashes", "a.txt"),
    ],
)
def test_requirements_file_parsing(line, file):
    assert requirements_file(line) == (file, "")


@pytest.mark.parametrize(
    "line",
    [
        "pip3 install copr-cli",
        "pip3 install -r a.txt",
        "pip3 install --require-hashes -r a.txt copr-cli",
        "pip3 install --require-hashes",
    ],
)
def test_requirements_file_parsing_refuses(line):
    file, problem = requirements_file(line)
    assert problem, file


def test_unhashed_requirements():
    data = """# comment
a==1.0 \\
    --hash=sha256:00 \\
    --hash=sha256:11
    # via b
b==2.0 --hash=sha256:22  # via c
c>=1.0 --hash=sha256:33
d==1.0
e
"""
    assert unhashed_requirements(data) == ["c>=1.0", "d==1.0", "e"]


def test_docs_requirements_pin_the_themes_material():
    lines = (ROOT / "requirements.in").read_text(encoding="utf-8").split("\n")
    names = [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]
    assert "mkdocs-material==9.7.6" in names
    for package in ("pillow", "cairosvg", "mkdocs-git-revision-date-localized-plugin"):
        # The exact name (pip treats `-`, `_` and `.` alike), then extras, a
        # version specifier, a marker, a URL, a comment or nothing:
        # `pillow-simd` is not `pillow`.
        name = r"[-_.]+".join(re.escape(part) for part in package.split("-"))
        exact = rf"{name}\s*(?:[\[<>=!~;@#]|$)"
        assert any(re.match(exact, n, re.IGNORECASE) for n in names), package
    locked = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    assert "mkdocs-material==9.7.6 " in locked


def test_brand_submodule_skips_recursive_clones():
    # `update = none` keeps `git clone --recursive` working for anyone without
    # access to the private theme; a build asks for it explicitly.
    section = ""
    got = {}
    for line in (ROOT / ".gitmodules").read_text(encoding="utf-8").split("\n"):
        line = line.strip()
        if line.startswith("["):
            section = line
            continue
        if section == '[submodule "brand"]' and "=" in line:
            key, value = line.split("=", 1)
            got[key.strip()] = value.strip()
    assert got == {
        "path": "brand",
        "url": "https://github.com/qubernetic/brand.git",
        "update": "none",
    }


def test_install_needs_no_apt():
    wf = load_workflow()
    for name in wf["jobs"]:
        for i, step in enumerate(steps_of(wf, name), 1):
            run = text(step.get("run"))
            assert "apt-get" not in run and "apt install" not in run, f"job {name} step {i}"
