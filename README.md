# argotests

Argo CD applications in the shapes that make source editing hard, so a tool can
be tested against them rather than against one repository that happens to be
handy.

Everything here renders ConfigMaps. Nothing runs, nothing pulls an image, and a
whole cluster of it costs nothing — the point is the *shape* of each source, not
what it deploys.

## What each shape is for

| Path | Shape | What it exercises |
|---|---|---|
| `helm/single-overlay` | chart in `prod/`, values above and beside it, one overlay | A kustomization can go in the parent, where both value files are already in reach |
| `helm/multi-overlay` | two overlays sharing a parent, driven by an ApplicationSet | The parent is taken, so the kustomization goes beside the chart and needs kustomize's load restrictor relaxed |
| `helm/values-inside` | values only inside the chart directory | Nothing above the chart to reach for |
| `helm/umbrella` | wrapper chart with a vendored `file://` dependency | Objects that come from a subchart, not the chart's own templates |
| `helm/no-values` | Application names no value files | Chart defaults only |
| `kustomize/plain` | `resources` and `patches`, one patch with a `target` block | Telling a resource file from a patch; removing either without disturbing the other |
| `kustomize/base-overlay` | overlay whose only resource is `../../base` | An object with no file here to edit |
| `kustomize/generators` | `configMapGenerator` reading a `.env` | An object built by the kustomization rather than declared |

The chart templates print `.Release.Namespace`, `.Release.Name` and which values
file won. `helm/single-overlay` also ships a CRD. Both are there so that a
conversion which quietly drops the namespace, the release name, the values order
or `--include-crds` shows up as a difference in the rendered output instead of
passing unnoticed.

## Applications

`argocd/` holds one Application per shape, plus one ApplicationSet. Apply the
directory to a cluster running Argo CD; every application points back at this
repository, which is public, so nothing needs credentials.
