# GitOps patterns Radar can edit safely

This catalog has 63 generic patterns: 37 supported, 23 not supported, one wrong, and two unsure. The wrong case can produce a pull request that leaves the deployed memory limit unchanged. These are predictions from Radar's code, backed by fixture renders and the checks described below. They are not results from opening live pull requests.

Each case links to its sources, how common it is, where the memory limit is set, the predicted edit or refusal, and a render command. Applications and ApplicationSets are in [argocd/](argocd/). Prevalence means common, occasional, or rare in the cited guidance and examples. It is not an adoption percentage. A refusal is an acceptable result; an ineffective edit is not.

| Case | Pattern | How common | Expected Radar result | Reason |
|---|---|---|---|---|
| **Repository layout** | | | | |
| [01-mono-envs](01-mono-envs/case.yaml) | Apps and environment entry points in one repository | Common | Supported | Edits the shared Deployment literal. Other readers can require scope confirmation. |
| [02-app-repo](02-app-repo/case.yaml) | Repository per application | Common | Supported | Edits the Deployment in the application's deploy directory. |
| [03-env-repo](03-env-repo/case.yaml) | Repository per environment | Occasional | Supported | Edits the production configuration source. |
| [04-config-repo](04-config-repo/case.yaml) | Configuration repository separate from app code | Common | Supported | Edits the configuration source without needing application code. |
| [05-env-branch](05-env-branch/case.yaml) | Branch per environment | Occasional | Supported | Edits the tracked branch and warns about promotion. The branch must exist. |
| **Directory sources and YAML memory locations** | | | | |
| [06-dir-recurse](06-dir-recurse/case.yaml) | Recursive plain YAML directories | Common | Supported | Honors recursion and edits the nested Deployment. |
| [07-dir-filters](07-dir-filters/case.yaml) | Include/exclude globs and skipped files | Occasional | Supported | Selects the deployable manifest, excluding operational files. |
| [08-yaml-anchor](08-yaml-anchor/case.yaml) | Shared scalar anchor and alias | Occasional | Not supported | `editor-refused`: changing the anchored scalar also changes aliases. |
| [09-multi-doc](09-multi-doc/case.yaml) | Several resources in one YAML stream | Common | Supported | Edits the Deployment document in the bundle. |
| **Application creation and environment discovery** | | | | |
| [10-app-tree](10-app-tree/case.yaml) | App of apps | Common | Supported | Follows the workload's child Application to its source. |
| [11-set-directories](11-set-directories/case.yaml) | ApplicationSet Git directory generator | Common | Supported | Edits the generated Application's workload source. |
| [12-set-files](12-set-files/case.yaml) | ApplicationSet per-environment config files | Common | Supported | Reads the generated Application's selected source path. |
| [13-set-list](13-set-list/case.yaml) | ApplicationSet explicit environment list | Common | Supported | Edits the source chosen by the generated Application. |
| [14-set-clusters](14-set-clusters/case.yaml) | ApplicationSet cluster label selection | Common | Supported | Edits the workload source when live membership is readable. |
| [15-set-matrix](15-set-matrix/case.yaml) | ApplicationSet app/environment matrix | Common | Supported | Edits the selected matrix member's workload source. |
| [16-set-merge](16-set-merge/case.yaml) | ApplicationSet environment merge overrides | Occasional | Supported | Uses the live Application and membership; offline Merge expansion is unavailable. |
| [17-team-app](17-team-app/case.yaml) | Application outside the control-plane namespace | Occasional | Supported | Namespace alone does not block the manifest edit. Argo CD must allow the Application. |
| [62-scm-teams](62-scm-teams/case.yaml) | Organization discovery with central config | Occasional | Supported | Edits the generated Application's config source; live membership resolves opaque discovery. |
| [63-pr-preview](63-pr-preview/case.yaml) | Pull-request preview pinned to its head SHA | Occasional | Not supported | `pinned-revision`: a new pull request does not move the deployed SHA. |
| **Git revisions** | | | | |
| [18-release-tag](18-release-tag/case.yaml) | Release tag pin | Common | Not supported | `pinned-revision`: the Application must move to a newer Git version. |
| [19-commit-pin](19-commit-pin/case.yaml) | Exact commit pin | Common | Not supported | `pinned-revision`: the Application must move to a newer Git version. |
| [61-git-range](61-git-range/case.yaml) | Git semver range with app-prefixed tags | Occasional | Unsure | Resolver tries a literal ref, not semver tags; exact provider/UI error is unverified. |
| **Multiple sources** | | | | |
| [20-git-sources](20-git-sources/case.yaml) | Several Git sources producing manifests | Occasional | Not supported | `generated-source`: Radar cannot combine several render sources. |
| [38-chart-values-ref](38-chart-values-ref/case.yaml) | Pinned Helm-repository chart plus Git values | Common | Supported | Edits `resources.limits.memory` in the Git values ref. |
| [39-oci-values-ref](39-oci-values-ref/case.yaml) | Pinned OCI chart plus Git values | Occasional | Supported | Edits the Git values ref after rendering the pinned chart. |
| **Helm sources and value shapes** | | | | |
| [21-helm-flat](21-helm-flat/case.yaml) | Local chart with a flat memory setting | Common | Supported | Edits `memoryLimit` in chart values. |
| [22-repo-inline](22-repo-inline/case.yaml) | Helm-repository chart with inline values | Common | Not supported | `generated-source`: the remote chart has no Git value file to edit. |
| [23-umbrella](23-umbrella/case.yaml) | Umbrella chart with a vendored subchart | Common | Supported | Edits `checkout.resources.limits.memory` in parent values. |
| [24-library-chart](24-library-chart/case.yaml) | Application chart using a library chart | Occasional | Supported | Edits `resources.limits.memory` in application values. |
| [25-global-values](25-global-values/case.yaml) | Shared `global.*` value | Occasional | Supported | Edits `global.memoryLimit`. |
| [26-container-list](26-container-list/case.yaml) | Values list per container | Occasional | Not supported | `list-item`: Radar cannot safely select the list item by name. |
| [27-resources-yaml](27-resources-yaml/case.yaml) | Nested resources passed through `toYaml` | Common | Supported | Edits `resources.limits.memory`. |
| [28-resources-tpl](28-resources-tpl/case.yaml) | Resources string evaluated through `tpl` | Occasional | Supported | The rendered dependency proves that `memoryLimit` controls this limit. |
| **Helm environment layers and render overrides** | | | | |
| [29-values-layers](29-values-layers/case.yaml) | Defaults, environment globs, and cluster values | Common | Supported | Edits the highest winning layer, the cluster values file. |
| [30-inline-values](30-inline-values/case.yaml) | Application `helm.values` string | Common | Not supported | `app-spec-values`: memory is set by the Application spec. |
| [31-values-object](31-values-object/case.yaml) | Application `helm.valuesObject` map | Common | Not supported | `app-spec-values`: memory is set by the Application spec. |
| [32-helm-parameter](32-helm-parameter/case.yaml) | Application Helm parameter | Common | Not supported | `app-spec-values`: memory is set by the Application spec. |
| [33-optional-values](33-optional-values/case.yaml) | `ignoreMissingValueFiles` | Occasional | Supported | Skips the absent file and edits the production file that sets memory. |
| [34-release-options](34-release-options/case.yaml) | Release name, namespace, and `skipCrds` | Occasional | Supported | Memory edit is correct. Radar's preview includes CRDs, so parity can warn. |
| [35-source-default](35-source-default/case.yaml) | `.argocd-source.yaml` Helm override | Occasional | Not supported | `argocd-source-override`: Radar detects the file that owns the parameter. |
| [36-source-app](36-source-app/case.yaml) | Namespace-prefixed Application source file | Occasional | WRONG | Radar misses the source file and edits chart defaults. Argo CD still renders 64Mi. |
| [37-build-env-values](37-build-env-values/case.yaml) | Values path using `ARGOCD_APP_NAME` | Occasional | Supported | Expands the value-file path and edits its memory key. |
| [40-chart-range](40-chart-range/case.yaml) | Helm chart semver range | Occasional | Not supported | `generated-source`: Radar cannot resolve the chart range like Argo CD. |
| **Kustomize memory locations and composition** | | | | |
| [41-base-overlay](41-base-overlay/case.yaml) | Shared base and environment overlay | Common | Supported | Edits the base Deployment literal after proving the overlay preserves it. |
| [42-strategic-file](42-strategic-file/case.yaml) | Strategic merge patch file | Common | Supported | Edits the memory scalar in the environment patch. |
| [43-json-file](43-json-file/case.yaml) | JSON6902 patch file | Common | Supported | Edits the operation value for the memory path. |
| [44-inline-merge](44-inline-merge/case.yaml) | Inline strategic merge patch | Occasional | Not supported | `editor-refused`: Radar will not rewrite the inline patch block. |
| [45-inline-json](45-inline-json/case.yaml) | Inline JSON6902 operation | Occasional | Not supported | `editor-refused`: no editable candidate changes the rendered limit. |
| [46-label-patch](46-label-patch/case.yaml) | Patch selected by labels | Occasional | Supported | Render proof locates the external patch's memory operation. |
| [47-resource-component](47-resource-component/case.yaml) | Reusable resource component | Occasional | Supported | Edits the component's resource patch. |
| [48-config-replacement](48-config-replacement/case.yaml) | ConfigMap replacement into memory | Occasional | Not supported | `editor-refused`: the replacement value is not an editable memory candidate. |
| [49-generated-memory](49-generated-memory/case.yaml) | Generated ConfigMap replacement | Occasional | Not supported | `editor-refused`: the generator input is not an editable memory candidate. |
| [50-remote-base](50-remote-base/case.yaml) | Pinned external Git base | Occasional | Not supported | `remote-base`: Radar does not fetch the external base. |
| [51-helm-in-kustomize](51-helm-in-kustomize/case.yaml) | Kustomize `helmCharts` with a vendored chart | Occasional | Not supported | `remote-base`: Radar refuses Helm inflation, including this local chart. |
| **Other source generators** | | | | |
| [52-jsonnet-app](52-jsonnet-app/case.yaml) | Jsonnet program | Occasional | Not supported | `generated-source`: Jsonnet produces the Deployment. |
| [53-plugin-render](53-plugin-render/case.yaml) | Config management sidecar plugin | Occasional | Not supported | `generated-source`: a plugin produces the manifests. |
| **Admission, autoscaling, and operator ownership** | | | | |
| [54-namespace-default](54-namespace-default/case.yaml) | LimitRange default with no template limit | Common | Supported | Adds an explicit Deployment limit; it does not edit the namespace default. |
| [55-vertical-policy](55-vertical-policy/case.yaml) | VPA controls the request-to-limit ratio | Occasional | Supported | Edits the template limit with `vpa-scales` and `vpa-ratio` warnings. |
| [56-operator-service](56-operator-service/case.yaml) | Operator CR owns the Deployment | Occasional | Unsure | Runtime tracking decides live route or source refusal. Radar does not trace the CR memory key. |
| **Application Kustomize overrides** | | | | |
| [57-application-patch](57-application-patch/case.yaml) | Application inline Kustomize memory patch | Occasional | Not supported | `app-spec-values`: the Application's patch sets memory. |
| [58-build-annotation](58-build-annotation/case.yaml) | Build variable in common annotations | Occasional | Not supported | `app-spec-values`: Radar cannot fill in this annotation variable. |
| [59-custom-kustomize](59-custom-kustomize/case.yaml) | Administrator-registered Kustomize version | Occasional | Not supported | `app-spec-values`: Radar cannot run the selected version. |
| [60-identity-options](60-identity-options/case.yaml) | Application namespace and name prefix | Occasional | Supported | Reproduces identity transformations and edits the source Deployment. |

## Wrong and unsure cases

- **WRONG: [36-source-app](36-source-app/case.yaml).** For an Application outside the `argocd` namespace, Argo CD reads its per-app source file as `.argocd-source-<namespace>_<app>.yaml` ([source-file contract](https://argo-cd.readthedocs.io/en/stable/user-guide/parameters/#store-overrides-in-git)). Radar looks only for `.argocd-source-<app>.yaml` and `.argocd-source.yaml`. Here the chart default and the source-file parameter both say 64Mi, so Radar and Argo CD agree before the edit. Radar then edits `apps/checkout/values.yaml`, but Argo CD's parameter still wins and keeps 64Mi. The PR does nothing. The case records all four renders.
- **UNSURE: [56-operator-service](56-operator-service/case.yaml).** Git holds a Knative Service, and the Knative controller creates the Deployment. What Radar does depends on how that Deployment is tracked at runtime. It either treats it as not managed by GitOps, or refuses because the Deployment isn't in the rendered source. Either way it's a refusal, not a PR. A live cluster decides which. See the [Knative architecture](https://knative.dev/docs/serving/architecture/).
- **UNSURE: [61-git-range](61-git-range/case.yaml).** Argo CD can track a semver range of app-prefixed tags. Radar doesn't pick matching tags, so it's expected to fail while planning, not open a wrong PR. The exact message hasn't been checked. See [Argo CD revision tracking](https://argo-cd.readthedocs.io/en/stable/user-guide/tracking_strategies/).

## How the expected results were set

Each expected result is a prediction from reading Radar's code, checked against offline renders of the fixture. None of them comes from a live run yet. The requested change is always 64Mi to 128Mi. Predictions assume a synced Application, a readable repository, a signed-in Git identity with write access, and a known Argo CD version. Missing permissions or controllers can stop a plan earlier.

Sources: the [Argo CD Application spec](https://argo-cd.readthedocs.io/en/stable/user-guide/application-specification/), [Helm guidance](https://helm.sh/docs/chart_best_practices/values/), [Kustomize documentation](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/), [Flux repository structures](https://fluxcd.io/flux/guides/repository-structure/), [Kostis's environment model](https://octopus.com/blog/how-to-model-your-gitops-environments), [Akuity's cluster add-ons workshop](https://docs.akuity.io/tutorials/cluster-addons-with-applicationsets/), [Argo example apps](https://github.com/argoproj/argocd-example-apps), [Argo CD Image Updater](https://argocd-image-updater.readthedocs.io/en/stable/basics/update-methods/) and the [Red Hat GitOps catalog](https://github.com/redhat-cop/gitops-catalog). Each `case.yaml` has its own URLs and how-common evidence. [research/](research/) has the notes.

To check every fixture renders a 64Mi limit:

```sh
python3 catalog/check-renders.py --output catalog/checks/renders.json
```

It needs Python with PyYAML, Helm, Kustomize, Jsonnet, and network access for remote bases and charts. Case 51 needs a Helm 3 binary named `helm3`, because Kustomize's Helm inflator passes a flag Helm 4 rejects.

Notes per case:
- **Runtime cases:** case 54 has no limit in Git, and a LimitRange gives the pods 64Mi. Case 56's Deployment is created by Knative. Case 55's VPA can change the limit on running pods.
- **Setup:** `generated-application.yaml` files are samples of what an ApplicationSet generates. Don't install them. Apps outside `argocd` need Argo CD's apps-in-any-namespace setup. Case 51 needs Helm inflation turned on, case 53 needs its plugin, and case 59 needs a registered Kustomize version.
- **Refs:** case 05 needs a `production` branch. Cases 18 and 19 need a tag and a commit that contain the catalog. Case 61 needs prefixed release tags, and case 63 needs an open labelled pull request.
- **Not covered:** private chart credentials, Helm downloader plugins, Kustomize function plugins and other operator APIs have no case here.
