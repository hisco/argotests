# GitOps patterns and what Radar does with them

Each folder here is one common way teams set a container's memory limit through Argo CD. For each one, the table says whether Radar's "fix it in Git" opens a pull request for it, and why. Every case deploys one Deployment with a 64Mi limit, and the requested change is 64Mi to 128Mi.

| Result | Cases |
|---|---|
| [Supported](#supported) | 33 |
| [Partly supported](#partly-supported) | 4 |
| Known bugs | 0 |
| [Not supported](#not-supported) | 25 |
| [Not verified yet](#not-verified-yet) | 1 |

Status: checked live on Argo CD v3.5.5 on 2026-10-19. 62 of the 63 cases ran; case 56 needs Knative and was not run. Every pull request Radar offered was applied to a copy of the repo and rendered by Argo CD itself, and only that limit changed.

Each `case.yaml` has the details: where the 64Mi is set, sources for the pattern, how common it is, the expected edit or refusal, and a render command.

## Supported

Radar opens a pull request that changes only this container's memory limit, in the file and key listed.

| Case | Pattern | How common | Why |
|---|---|---|---|
| [02-app-repo](02-app-repo/case.yaml) | One application repository | Common | Edits the Deployment in the app's deploy folder. |
| [03-env-repo](03-env-repo/case.yaml) | One production configuration repository | Occasional | Edits the Deployment in the environment's repo. |
| [04-config-repo](04-config-repo/case.yaml) | Configuration separated from application code | Common | Edits the config repo. The app's code repo isn't needed. |
| [06-dir-recurse](06-dir-recurse/case.yaml) | Recursive plain manifests | Common | Follows recurse and edits the nested Deployment. |
| [07-dir-filters](07-dir-filters/case.yaml) | Directory include and exclude | Occasional | Applies include and exclude the way Argo CD does and edits the deployed file. |
| [09-multi-doc](09-multi-doc/case.yaml) | Deployment in a multi-document bundle | Common | Edits the Deployment's document inside the multi-document file. |
| [10-app-tree](10-app-tree/case.yaml) | App of apps | Common | Follows the child Application to its source. |
| [11-set-directories](11-set-directories/case.yaml) | ApplicationSet Git directories | Common | Edits the source of the Application the generator made. |
| [12-set-files](12-set-files/case.yaml) | ApplicationSet environment files | Common | Edits the source path the generated Application reads. |
| [13-set-list](13-set-list/case.yaml) | ApplicationSet explicit environment list | Common | Edits the source the generated Application reads. |
| [14-set-clusters](14-set-clusters/case.yaml) | ApplicationSet cluster selection | Common | Edits the source of the Application the cluster generator made, read from the live Application. |
| [15-set-matrix](15-set-matrix/case.yaml) | ApplicationSet app and environment matrix | Common | Edits the source of the matrix member that deploys this workload. |
| [16-set-merge](16-set-merge/case.yaml) | ApplicationSet environment overrides | Occasional | Edits the source of the Application the merge generator made, read from the live Application. |
| [17-team-app](17-team-app/case.yaml) | Application in a team namespace | Occasional | An Application outside the argocd namespace is handled the same way. Argo CD itself must be set up to allow it. |
| [21-helm-flat](21-helm-flat/case.yaml) | Flat chart values | Common | Edits `memoryLimit` in the chart's values. |
| [23-umbrella](23-umbrella/case.yaml) | Umbrella chart | Common | Edits `checkout.resources.limits.memory` in the parent chart's values. |
| [24-library-chart](24-library-chart/case.yaml) | Shared library chart | Occasional | Edits `resources.limits.memory` in the app chart's values. |
| [25-global-values](25-global-values/case.yaml) | Global chart values | Occasional | Edits `global.memoryLimit`. |
| [27-resources-yaml](27-resources-yaml/case.yaml) | Nested resources through toYaml | Common | Edits `resources.limits.memory` that the template passes through `toYaml`. |
| [28-resources-tpl](28-resources-tpl/case.yaml) | Resources through tpl | Occasional | Edits `memoryLimit`, after proving by render that the `tpl` string uses it. |
| [29-values-layers](29-values-layers/case.yaml) | Environment and cluster value layers | Common | Edits the value file that wins for this environment, here the cluster file. |
| [33-optional-values](33-optional-values/case.yaml) | Optional environment values | Occasional | Skips the missing optional file and edits the file that sets the limit. |
| [34-release-options](34-release-options/case.yaml) | Release and namespace options | Occasional | Radar's render follows skipCrds the way Argo CD does, so it opens the PR. The edit was checked with Argo CD's own render. |
| [37-build-env-values](37-build-env-values/case.yaml) | Build environment value path | Occasional | Fills in `$ARGOCD_APP_NAME` in the value-file path and edits that file. |
| [38-chart-values-ref](38-chart-values-ref/case.yaml) | Helm repository chart and Git values | Common | The chart comes from a Helm repo and values from Git (`$values`). Edits the Git value file. |
| [39-oci-values-ref](39-oci-values-ref/case.yaml) | OCI chart and Git values | Occasional | The chart comes from a public OCI registry (ghcr.io) and values from Git. Edits the Git value file. Checked live: the change reached 128Mi. |
| [42-strategic-file](42-strategic-file/case.yaml) | Strategic merge patch file | Common | Edits the limit in the environment's patch file. |
| [43-json-file](43-json-file/case.yaml) | JSON6902 patch file | Common | Edits the value of the JSON6902 operation for the memory path. |
| [46-label-patch](46-label-patch/case.yaml) | Patch target by label selector | Occasional | Edits the patch file that a label selector applies. |
| [47-resource-component](47-resource-component/case.yaml) | Reusable resource component | Occasional | Edits the component's patch. |
| [54-namespace-default](54-namespace-default/case.yaml) | LimitRange supplies the Pod default | Common | Git sets no limit; a LimitRange default does. Radar adds an explicit limit to this Deployment instead of changing the default for the whole namespace. |
| [60-identity-options](60-identity-options/case.yaml) | Application changes namespace and name | Occasional | Applies the Application's namespace and name prefix the way Argo CD does and edits the source Deployment. |
| [62-scm-teams](62-scm-teams/case.yaml) | Organization discovery with central configuration | Occasional | Edits the shared config source of the Application the SCM generator made, read from the live Application. |

## Partly supported

Radar finds the right change, with a condition or side effect you should know about. The reason says which.

| Case | Pattern | How common | Why |
|---|---|---|---|
| [01-mono-envs](01-mono-envs/case.yaml) | Apps and environments in one repository | Common | Opens the PR. The file it edits could be read by other environments, so Radar warns that apps it can't see may change too. It doesn't name them. |
| [05-env-branch](05-env-branch/case.yaml) | Production branch promotion | Occasional | Opens the PR into the branch the Application tracks, and warns that the next promotion into that branch can overwrite it. |
| [41-base-overlay](41-base-overlay/case.yaml) | Base plus production overlay | Common | Opens the PR, editing the limit in the shared base. Every overlay built on that base changes too. Radar warns that apps it can't see may change, but it doesn't add a patch for just one environment. |
| [55-vertical-policy](55-vertical-policy/case.yaml) | VPA scales limits from the template ratio | Occasional | Edits the template limit, and warns that VPA can change the limit on running pods. |

## Not supported

Radar refuses and says why. No pull request is opened. This is on purpose: Radar can't make the change safely in this setup.

| Case | Pattern | How common | Why |
|---|---|---|---|
| [08-yaml-anchor](08-yaml-anchor/case.yaml) | Shared YAML scalar anchor | Occasional | The limit is a YAML anchor that other places reuse. Changing it would change them too, so Radar refuses. |
| [18-release-tag](18-release-tag/case.yaml) | Release tag pin | Common | The Application deploys a fixed tag. A PR to a branch wouldn't change what's deployed. The Application has to move to a newer tag. |
| [19-commit-pin](19-commit-pin/case.yaml) | Exact commit pin | Common | The Application deploys a fixed commit. A PR wouldn't change what's deployed. |
| [20-git-sources](20-git-sources/case.yaml) | Merged Git manifest sources | Occasional | Several Git sources each produce manifests. Radar can't combine them into one render. |
| [22-repo-inline](22-repo-inline/case.yaml) | Remote chart with inline values | Common | The chart comes from a Helm repo and the values are inline in the Application. There's no Git file to edit. |
| [26-container-list](26-container-list/case.yaml) | Values list per container | Occasional | Containers are a list in values. Radar won't pick a list item by position, so it refuses. |
| [30-inline-values](30-inline-values/case.yaml) | Inline YAML values | Common | The limit is set in the Application's `helm.values`, not in a Git file Radar edits. Change it in the Application. |
| [31-values-object](31-values-object/case.yaml) | Inline valuesObject | Common | The limit is set in the Application's `helm.valuesObject`. Change it in the Application. |
| [32-helm-parameter](32-helm-parameter/case.yaml) | Helm parameter override | Common | The limit is a Helm parameter in the Application. Change it in the Application. |
| [35-source-default](35-source-default/case.yaml) | Repository source override | Occasional | A `.argocd-source.yaml` file sets the limit as a parameter. Radar finds it and says to change it there. |
| [36-source-app](36-source-app/case.yaml) | Namespaced application source override | Occasional | The limit is set by a parameter in `.argocd-source-<namespace>_<app>.yaml`, the per-app file Argo CD reads for an Application outside the argocd namespace. Radar finds it, refuses, and says to change it in that file. |
| [40-chart-range](40-chart-range/case.yaml) | Chart version range | Occasional | The chart version is a range. Radar can't resolve it the way Argo CD does, so it can't be sure which chart is live. |
| [44-inline-merge](44-inline-merge/case.yaml) | Inline strategic merge patch | Occasional | The patch is written inline in kustomization.yaml. Radar won't rewrite an inline patch block. |
| [45-inline-json](45-inline-json/case.yaml) | Inline JSON6902 patch | Occasional | The JSON6902 operation is inline in kustomization.yaml. Radar won't rewrite it. |
| [48-config-replacement](48-config-replacement/case.yaml) | ConfigMap field replacement | Occasional | A Kustomize replacement copies the limit from a ConfigMap. Radar doesn't edit through replacements. |
| [49-generated-memory](49-generated-memory/case.yaml) | Generated ConfigMap replacement | Occasional | The limit comes from a generated ConfigMap through a replacement. Radar doesn't edit generator inputs. |
| [50-remote-base](50-remote-base/case.yaml) | Pinned remote Kustomize base | Occasional | The base is in another Git repo. Radar doesn't fetch remote Kustomize bases. |
| [51-helm-in-kustomize](51-helm-in-kustomize/case.yaml) | Vendored Helm chart in Kustomize | Occasional | Kustomize inflates a Helm chart (`helmCharts`). Radar refuses and says it doesn't render that yet, even when the chart is in the repo. |
| [52-jsonnet-app](52-jsonnet-app/case.yaml) | Jsonnet source | Occasional | Jsonnet code builds the Deployment. Radar doesn't edit Jsonnet. |
| [53-plugin-render](53-plugin-render/case.yaml) | Config management plugin | Occasional | A config management plugin builds the manifests. Radar can't run it. |
| [57-application-patch](57-application-patch/case.yaml) | Application inline Kustomize patch | Occasional | A Kustomize patch inside the Application sets the limit. Change it in the Application. |
| [58-build-annotation](58-build-annotation/case.yaml) | Build environment in annotation | Occasional | The Application's Kustomize options use a build variable Radar can't fill in, so it can't reproduce the render. |
| [59-custom-kustomize](59-custom-kustomize/case.yaml) | Application selects a Kustomize version | Occasional | The Application uses an admin-registered Kustomize version Radar can't run. |
| [61-git-range](61-git-range/case.yaml) | Git semver range and app tag prefix | Occasional | The Application deploys the newest tag that matches a range, so a PR into a branch won't reach it. Radar refuses and says so. |
| [63-pr-preview](63-pr-preview/case.yaml) | Pull-request preview at its head commit | Occasional | A PR preview app is pinned to the PR's head commit. A new PR wouldn't change it. |

## Not verified yet

No pull request is expected, but Radar's exact behaviour hasn't been checked on a live cluster.

| Case | Pattern | How common | Why |
|---|---|---|---|
| [56-operator-service](56-operator-service/case.yaml) | Operator owns the Deployment | Occasional | Not run live: needs Knative installed. Knative creates the Deployment from a Service in Git. Radar is expected to refuse either way, but which message it shows isn't checked. |

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
