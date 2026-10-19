# Kustomize, generated sources and controller-owned values

## Which patterns are established outside Radar?

### Takeaway

Bases, overlays and patch files are standard GitOps building blocks. Components and replacements are documented compositions. Their prevalence labels are qualitative, based on the sources below, not a deployment survey.

### Cited findings

- Kubernetes documents bases, overlays, file and inline patches, strategic merge, JSON6902 and label selectors. It even recommends a separate patch for memory limits. These support cases 41-46. [Kubernetes task](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- Argo CD maintains a Kustomize application example. The Red Hat Community of Practice catalog also uses bases and overlays. Its Jenkins overlay directly includes `../../base`. These are independent examples behind the common label on case 41. [Argo CD example](https://github.com/argoproj/argocd-example-apps/tree/master/kustomize-guestbook), [GitOps catalog](https://github.com/redhat-cop/gitops-catalog), [Jenkins overlay](https://raw.githubusercontent.com/redhat-cop/gitops-catalog/main/jenkins2/overlays/default/kustomization.yaml)
- Upstream Kustomize demonstrates optional components. A Red Hat Community of Practice multi-cluster template composes cluster groups using `kind: Component`. Case 47 represents reusable component patches. [Kustomize example](https://github.com/kubernetes-sigs/kustomize/blob/master/examples/components.md), [platform template](https://github.com/redhat-cop/gitops-standards-repo-template)
- Replacements copy a resource field into selected targets. ConfigMap generators can read environment files. Cases 48-49 combine those supported Kustomize operations to supply a memory setting. [Kustomize reference index](https://kubectl.docs.kubernetes.io/references/kustomize/kustomization/), [Kubernetes task](https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/)
- Remote Kustomize directories accept a Git `ref`. Case 50 consumes podinfo's versioned base and applies local resource settings. [Remote build guide](https://github.com/kubernetes-sigs/kustomize/blob/master/examples/remoteBuild.md), [podinfo 6.7.1](https://github.com/stefanprodan/podinfo/tree/6.7.1/kustomize)
- Kustomize can inflate Helm charts before applying transformers. Case 51 uses a local vendored chart, so no remote chart is needed. [Kustomize chart guide](https://github.com/kubernetes-sigs/kustomize/blob/master/examples/chart.md)
- Argo CD supports Jsonnet and repo-server sidecar plugins. Cases 52-53 use an external variable and a named plugin. [Jsonnet guide](https://argo-cd.readthedocs.io/en/stable/user-guide/jsonnet/), [Jsonnet example](https://github.com/argoproj/argocd-example-apps/tree/master/jsonnet-guestbook), [plugin installation and environment](https://argo-cd.readthedocs.io/en/stable/operator-manual/config-management-plugins/)
- A LimitRange defaults newly admitted Pods. It does not rewrite the Deployment template. Case 54 keeps that distinction. [Namespace memory defaults](https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/)
- A VPA changes Pod requests rather than the Deployment template. With RequestsAndLimits, limits are scaled from the template ratio. Case 55 records both a ratio-bearing template and a separate absent-limit example. [VPA quickstart](https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/quickstart.md), [VPA API](https://github.com/kubernetes/autoscaler/blob/master/vertical-pod-autoscaler/docs/api.md)
- A Knative Service creates immutable Revisions and controls child resources. Its controller-generated Deployment is not a source manifest. Case 56 stores the CR and leaves its generated Deployment absent. [Creating Services](https://knative.dev/docs/serving/services/creating-services/), [architecture](https://knative.dev/docs/serving/architecture/), [scale bounds](https://knative.dev/docs/serving/autoscaling/scale-bounds/)
- Argo CD permits Application Kustomize patches, build-variable annotations, selected binary versions and identity overrides. Cases 57-60 cover those changes to the render. [Argo CD Kustomize guide](https://argo-cd.readthedocs.io/en/stable/user-guide/kustomize/), [build environment](https://argo-cd.readthedocs.io/en/stable/user-guide/build-environment/)

### Inferences

- Common means this pattern appears in the main Kubernetes workflow and independent GitOps examples. Occasional means documented and useful within a narrower workflow. No evidence here measures market share.
- ConfigMap-to-resource replacements are instances of the generic replacement mechanism. The sources establish the mechanism, rather than claiming that this exact memory field is widespread.

### Gaps

- Direct fetches of several kubectl reference subpages failed in the research browser. The fetched reference index and Kubernetes task independently describe these features.
- No defensible adoption percentages were found. Repository star counts were not treated as pattern usage counts.

## What does the current Radar implementation do?

### Takeaway

The eight supported predictions edit proven file nodes. Eleven patterns are refused. The Knative child Deployment remains unsure because live tracking determines which route is reached. No wrong PR is established within these twenty cases.

### Cited findings


### Inferences

- A controller-owned Deployment should be exercised through the full live service, not only a locator request that assumes it already has an Application owner.
- The wording on replacement refusals is less precise than the reason detail. This is not evidence of a wrong pull request.

### Gaps

- Offline renders cannot settle the child tracking metadata or Application inventory in case 56.
- Full service checks require a running Argo CD cluster and user permissions. They were traced, not executed here.

## What was verified, and what remains outside these fixtures?

### Takeaway

All twenty feasible source renders were checked. Eighteen produce one matching Deployment with 64Mi. Case 54 intentionally leaves the Deployment limit absent. Case 56 intentionally produces only a CR.

### Cited findings

- Each case stores its command and result in `render_check`. The local checks used Kustomize 5.6.0, Helm 3.19.0 for chart inflation, go-jsonnet 0.21.0 and POSIX sh with sed for the CMP command.
- Kustomize 5.6.0 invokes a Helm version flag that Helm 4.3.0 rejects. Repeating case 51 with Helm 3.19.0 produced the expected Deployment. Its command selects a `helm3` executable on PATH.
- The remote base in case 50 was fetched and built at tag 6.7.1. Its original container name is `podinfod`, recorded in the case. The overlay renames its Deployment and sets its HPA bounds to one.
- Case 53 proves the plugin's generate command, not sidecar installation. The plugin configuration is included outside the Application source path. An administrator must install it using Argo CD's plugin workflow. [Plugin installation](https://argo-cd.readthedocs.io/en/stable/operator-manual/config-management-plugins/)

### Inferences

- Applying all Applications still requires compatible Argo CD tooling and the prerequisite CRDs/controllers called out in each case. The catalog is not proof that those controllers are installed.

### Gaps

- VPA admission, LimitRange admission, Knative reconciliation and plugin sidecar registration were not run. An offline renderer cannot honestly invent their resulting live resources.
- A missing-limit VPA example cannot guarantee 64Mi. It is retained outside the Application source path in case 55 rather than passed off as rendered admission output.
- Case 56 represents the generic controller-owned Deployment pattern. It does not claim that every operator API has the same tracking metadata. Case 53 represents plugin-generated output without claiming compatibility with every plugin's own input format.
