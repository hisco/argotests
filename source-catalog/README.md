# source-catalog

Argo CD fixtures for Radar's "Edit the source file" route: Git doesn't set the
memory limit (and, for plain and hpa, the replica count), so a pull request has
to add the value to a source file.

| Folder | Shape |
|---|---|
| plain | plain directory, no memory limit, no replicas |
| kustomize | base plus a prod overlay, no memory limit |
| helm | local chart whose values set requests only |
| hpa | Deployment scaled by a HorizontalPodAutoscaler (min 1, max 3) |
