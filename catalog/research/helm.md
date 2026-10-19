# Helm sources and overrides

## Which patterns have public evidence?

### Takeaway
The fixtures cover standard Helm inputs and Argo CD's documented source options. Prevalence labels are qualitative. Public examples establish that a pattern exists, not how many teams use it.

### Cited Findings
- Flat settings, nested maps, and lists are documented chart interfaces. Cases 21, 26, and 27 cover those shapes. [Helm values guidance](https://helm.sh/docs/chart_best_practices/values/).
- Parent charts can override subchart values and share globals. Cases 23 and 25 cover both. [Helm subcharts](https://helm.sh/docs/chart_template_guide/subcharts_and_globals/).
- Library charts supply shared templates to application charts. Case 24 vendors a small library. [Helm libraries](https://helm.sh/docs/topics/library_charts/).
- `tpl` evaluates a value as a template. Case 28 passes a resources string that reads a separate memory setting. [Helm template guidance](https://helm.sh/docs/howto/charts_tips_and_tricks/).
- Podinfo 6.7.1 renders resources through `toYaml`. Case 27 uses that interface. Cases 22 and 38-40 use the upstream chart. [Pinned upstream template](https://raw.githubusercontent.com/stefanprodan/podinfo/6.7.1/charts/podinfo/templates/deployment.yaml).
- Environment hierarchies and chart-plus-values sources have published runnable examples. Cases 29, 38, and 39 cover them. [Kostis's Helm environment guide](https://octopus.com/blog/helm-values-argocd).
- Argo CD offers inline values, valuesObject, parameters, optional value files, release options, and OCI charts. Cases 22 and 30-34 cover these inputs. [Argo CD Helm integration](https://argo-cd.readthedocs.io/en/stable/user-guide/helm/).
- Build variables can select inputs. Case 37 selects a values file by Application name. [Argo CD build environment](https://argo-cd.readthedocs.io/en/stable/user-guide/build-environment/).
- Source files can override Helm settings. Applications outside the control-plane namespace require a namespace prefix in the application-specific filename. Cases 35 and 36 cover both forms. [Argo CD stored overrides](https://argo-cd.readthedocs.io/en/stable/user-guide/parameters/#store-overrides-in-git).
- Multiple sources can supply Git values to a remote chart. Chart revisions can track semver ranges. Cases 38-40 cover these combinations. [Multiple sources](https://argo-cd.readthedocs.io/en/stable/user-guide/multiple_sources/), [revision tracking](https://argo-cd.readthedocs.io/en/stable/user-guide/tracking_strategies/).
- Akuity's workshop combines external charts, per-cluster Git values, and ignoreMissingValueFiles. Cases 33 and 38 cite this concrete example. [Akuity cluster add-ons tutorial](https://docs.akuity.io/tutorials/cluster-addons-with-applicationsets/).
- Argo CD Image Updater writes source parameter files and documents the namespace-prefixed filename. Case 36 cites this implementation alongside the Argo CD contract. [argoproj-labs write-back guide](https://argocd-image-updater.readthedocs.io/en/stable/basics/update-methods/).

### Inferences
- Basic values maps and file layering are common because they appear in both tool documentation and public deployment guides. Specialized options are marked occasional. No numerical adoption claim is made.
- The [Red Hat community catalog](https://raw.githubusercontent.com/redhat-cop/gitops-catalog/main/README.md) is additional evidence for bases, overlays, and pinned remote references. It is a Kustomize catalog, so it is not evidence for Helm-specific adoption.

### Gaps
- No source found supplies a representative adoption rate for these patterns.

## How does Radar handle these cases?

### Takeaway
Radar finds scalar settings by rendering changed values, selects the highest layer that sets the key, then checks the edited render. It refuses list items and values owned by Application specs. A namespaced source-file override can escape discovery and defeat the proposed change.

### Cited Findings

### Inferences
- Case 36 is WRONG. Radar edits the chart's 64Mi default, while Argo CD keeps applying the source-file 64Mi parameter. Both baseline renders agree, so the service's current-value and parity checks pass. The fixture uses a documented namespace feature, not a private repository convention.
- Case 34 can show a parity warning if the skipped CRD is absent. Its memory edit is correct, so that warning alone does not make the case WRONG.

### Gaps
- A live Radar session was not used to open PRs. The predictions cite the backend and the exact UI wording. Shared catalog checks can run the exported locator without changing Radar.

## What was verified and what remains?

### Takeaway
All 20 fixtures render with the local Helm 4.3.0 CLI. Each produces one Deployment with one replica, the pinned podinfo image, a 16Mi request, and a 64Mi limit.

### Cited Findings
- Each case records its command and checked fields in `render_check`. Remote HTTP and OCI chart downloads succeeded. The OCI syntax follows [Argo CD's chart example](https://argo-cd.readthedocs.io/en/stable/user-guide/helm/).
- Case 36 also checks a proposed 128Mi values change. The source-file parameter leaves the rendered limit at 64Mi. Its `redteam_check` records the reproducer.
- Case 40 uses the declared `6.7.*` range during validation. It resolved to chart 6.7.1. The image remains explicitly pinned. [Argo CD range semantics](https://argo-cd.readthedocs.io/en/stable/user-guide/tracking_strategies/).

### Inferences
- Render success proves the fixtures' memory values. It does not prove a cluster accepts every resource, or that a future mutable registry returns identical bytes.

### Gaps
- No Kubernetes cluster was changed. Applications outside argocd require the usual Argo CD namespace configuration before installation.
- Private registry authentication, remote Helm plugins, chart archive size limits, and malformed charts were not separate fixtures. They require environment or invalid-input scenarios rather than another repository layout. They are not claimed supported by these fixtures.
