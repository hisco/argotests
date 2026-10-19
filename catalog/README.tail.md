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
