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
| service | Deployment plus a Service whose type Git sets (ClusterIP) |
| limitrange | no memory limit in Git; the namespace's LimitRange supplies a 64Mi default |
| links | a symbolic link no Application reads |
| overlay-patch | base plus a prod overlay whose patch file sets replicas and a memory request, no memory limit |
| shared | plain directory read by an Argo CD Application and by Flux Kustomizations applied by hand |
| strict | app folder plus a second Kustomize folder (reader) whose JSON patch test only passes while the container has no limits |
