# flux-catalog

Flux Kustomization fixtures for Radar's pull request route. The GitRepository and
Kustomization objects that read these folders are applied by hand, except
parent/clusters/child.yaml, which a parent Kustomization applies.

| Folder | Shape |
|---|---|
| plain | plain directory, no kustomization.yaml |
| overlay | base plus a prod overlay with a patch file |
| components | base plus a Kustomize component that sets the memory limit |
| images | spec.images on a Kustomization applied by hand |
| substitute | postBuild substitution (refused) |
| parent | a child Kustomization with spec.images and spec.patches, applied by a parent (refused for those values) |
| verify | GitRepository with spec.verify (refused) |
| sparse | GitRepository with sparseCheckout (refused) |
