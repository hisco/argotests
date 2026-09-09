#!/usr/bin/env python3
"""Compare two sets of rendered Kubernetes objects by identity.

An explicit "annotations: null" from a chart template and an absent key are the
same object to the API server, and kustomize drops the null when it re-emits, so
nulls are normalised away before comparing. Argo's own tracking annotations and
labels are dropped too: they are stamped after rendering and say nothing about
whether the source produced the same thing.
"""
import sys, yaml

ARGO_KEYS = {"argocd.argoproj.io/tracking-id", "kubectl.kubernetes.io/last-applied-configuration"}
ARGO_LABELS = {"app.kubernetes.io/instance"}

def strip(x):
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if v is not None}
    if isinstance(x, list):
        return [strip(v) for v in x]
    return x

def clean(d):
    d = strip(d)
    m = d.get("metadata") or {}
    for f in ("creationTimestamp", "resourceVersion", "uid", "generation", "managedFields",
              "namespace" if False else "___"):
        m.pop(f, None)
    for k in list((m.get("annotations") or {})):
        if k in ARGO_KEYS:
            m["annotations"].pop(k)
    if m.get("annotations") == {}:
        m.pop("annotations")
    for k in list((m.get("labels") or {})):
        if k in ARGO_LABELS:
            m["labels"].pop(k)
    if m.get("labels") == {}:
        m.pop("labels")
    d.pop("status", None)
    return d

# Not part of any application: the API server puts this in every namespace.
IGNORE_NAMES = {"kube-root-ca.crt"}

def load(path):
    out = {}
    docs = []
    for d in yaml.safe_load_all(open(path)):
        if not isinstance(d, dict):
            continue
        # kubectl -o yaml wraps everything in a List. Reading only top-level
        # documents found nothing and called it a match, which is the one
        # outcome a comparison must never produce by accident.
        if d.get("kind") == "List":
            docs.extend(d.get("items") or [])
        elif "kind" in d:
            docs.append(d)
    for d in docs:
        m = d.get("metadata") or {}
        if m.get("name") in IGNORE_NAMES:
            continue
        out[(d.get("apiVersion", ""), d["kind"], m.get("namespace", ""), m.get("name", ""))] = clean(d)
    if not out:
        raise SystemExit(f"{path}: no objects read — refusing to call that a match")
    return out

a, b = load(sys.argv[1]), load(sys.argv[2])
label = sys.argv[3] if len(sys.argv) > 3 else ""
onlyA, onlyB = sorted(set(a) - set(b)), sorted(set(b) - set(a))
diff = sorted(k for k in set(a) & set(b) if a[k] != b[k])
same = not onlyA and not onlyB and not diff
print(f"{label:26} before={len(a):3} after={len(b):3}  {'IDENTICAL' if same else 'DIFFERS'}")
for k in onlyA[:5]: print(f"      lost:    {k[1]}/{k[3]}")
for k in onlyB[:5]: print(f"      gained:  {k[1]}/{k[3]}")
for k in diff[:5]:
    print(f"      changed: {k[1]}/{k[3]}")
    da, db = a[k].get("data", {}), b[k].get("data", {})
    for key in sorted(set(da) | set(db)):
        if da.get(key) != db.get(key):
            print(f"         {key}: {da.get(key)!r} -> {db.get(key)!r}")
sys.exit(0 if same else 1)
