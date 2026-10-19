# Frames

Workloads that keep getting OOMKilled (podinfo asks for 200 MB at start, the limit is 64Mi), each set up in one GitOps shape, so "Change memory limit" shows on their pods. Used for before/after screenshots of Radar's fix-it-in-Git dialog.

- `a-child`: an app-of-apps child Application whose `helm.values` string sets the limit. Apply `argocd/a-child.yaml`.
- `b-template-literal`: a local chart whose template writes the limit as a literal. Apply `argocd/b-template-literal.yaml`.
- `c-inline-patch`: a kustomization whose inline patch sets the limit. Apply `argocd/c-inline-patch.yaml`.
