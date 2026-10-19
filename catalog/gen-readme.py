#!/usr/bin/env python3
"""Build catalog/README.md from each case.yaml. Run from the repository root."""

import glob
import os

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))

SECTIONS = [
    ("full", "Supported", "Radar opens a pull request that changes only this container's memory limit, in the file and key listed."),
    ("partial", "Partly supported", "Radar finds the right change, with a condition or side effect you should know about. The reason says which."),
    ("bug", "Known bugs", "Radar gets these wrong: a pull request that changes nothing, or a refusal of a setup it should handle. These are bugs, not limits we accept."),
    ("none", "Not supported", "Radar refuses and says why. No pull request is opened. This is on purpose: Radar can't make the change safely in this setup."),
    ("unverified", "Not verified yet", "No pull request is expected, but Radar's exact behaviour hasn't been checked on a live cluster."),
]


def load():
    cases = []
    for path in sorted(glob.glob(os.path.join(HERE, "*", "case.yaml"))):
        with open(path) as f:
            c = yaml.safe_load(f)
        c["_dir"] = os.path.basename(os.path.dirname(path))
        cases.append(c)
    return cases


def main():
    cases = load()
    count = {key: sum(1 for c in cases if c["support"] == key) for key, _, _ in SECTIONS}
    out = [
        "# GitOps patterns and what Radar does with them",
        "",
        "Each folder here is one common way teams set a container's memory limit through Argo CD. For each one, the table says whether Radar's \"fix it in Git\" opens a pull request for it, and why. Every case deploys one Deployment with a 64Mi limit, and the requested change is 64Mi to 128Mi.",
        "",
        "| Result | Cases |",
        "|---|---|",
    ]
    for key, title, _ in SECTIONS:
        out.append(f"| [{title}](#{title.lower().replace(' ', '-')}) | {count[key]} |")
    out += [
        "",
        "Status: checked live on Argo CD v3.5.5 on 2026-10-19. 62 of the 63 cases ran; case 56 needs Knative and was not run. Every pull request Radar offered was applied to a copy of the repo and rendered by Argo CD itself, and only that limit changed, except in the known bugs.",
        "",
        "Each `case.yaml` has the details: where the 64Mi is set, sources for the pattern, how common it is, the expected edit or refusal, and a render command.",
        "",
    ]
    for key, title, meaning in SECTIONS:
        rows = [c for c in cases if c["support"] == key]
        if not rows:
            continue
        out += [f"## {title}", "", meaning, "", "| Case | Pattern | How common | Why |", "|---|---|---|---|"]
        for c in rows:
            level = (c.get("prevalence") or {}).get("level", "").capitalize()
            why = c["support_why"].replace("|", "\\|")
            out.append(f"| [{c['_dir']}]({c['_dir']}/case.yaml) | {c['title']} | {level} | {why} |")
        out.append("")
    with open(os.path.join(HERE, "README.tail.md")) as f:
        out.append(f.read().rstrip() + "\n")
    with open(os.path.join(HERE, "README.md"), "w") as f:
        f.write("\n".join(out))


if __name__ == "__main__":
    main()
