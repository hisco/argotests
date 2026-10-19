# Repository layouts, plain YAML, Application creation, and revisions

## Which patterns have public evidence?

### Takeaway

Cases 01-20 and 61-63 cover documented layouts and Application creation methods. Prevalence labels are qualitative. They are based on official guidance and public examples, not an adoption survey.

### Cited findings

- Flux documents monorepos, repository per environment, and repository per app. It calls keeping deployment files beside app source common. These support cases 01-03. [Flux repository structure](https://fluxcd.io/flux/guides/repository-structure/)
- Kostis Kapelonis publishes an environment-per-folder model and discusses separate production repositories. The companion article critiques branch-per-environment workflows. These support cases 01, 03, and 05. [Environment model](https://octopus.com/blog/how-to-model-your-gitops-environments), [environment branches](https://octopus.com/blog/stop-using-branches-deploying-different-gitops-environments)
- Argo CD recommends a separate configuration repository. This supports case 04. [Best practices](https://argo-cd.readthedocs.io/en/stable/user-guide/best_practices/)
- Directory sources support recursive discovery, include/exclude globs, and a skip-file comment. Cases 06-07 exercise these controls. [Directory sources](https://argo-cd.readthedocs.io/en/stable/user-guide/directory/)
- YAML streams and anchors are documented Kubernetes authoring techniques. Cases 08-09 preserve their actual syntax. [Helm YAML techniques](https://helm.sh/docs/v3/chart_template_guide/yaml_techniques/)
- App of apps appears in the bootstrapping guide. Applications outside the control-plane namespace require explicit configuration. These support cases 10 and 17. [Bootstrapping](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/), [Application namespaces](https://argo-cd.readthedocs.io/en/stable/operator-manual/app-any-namespace/)
- ApplicationSet has Git directory/file, List, Cluster, Matrix, and Merge generators. Cases 11-16 use those forms. [Git](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Git/), [List](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-List/), [Cluster](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Cluster/), [Matrix](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Matrix/), [Merge](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Merge/)
- The Argo example repository includes app of apps and examples for each of these generator types. This is evidence of maintained examples, not a usage count. [Argo example apps](https://github.com/argoproj/argocd-example-apps)
- Branches, tags, and commit pins are supported deployment strategies. Cases 05, 18, and 19 distinguish them. [Tracking strategies](https://argo-cd.readthedocs.io/en/stable/user-guide/tracking_strategies/)
- Multiple sources render independently and their outputs are combined. Case 20 combines a Deployment directory and a shared ConfigMap directory. [Multiple sources](https://argo-cd.readthedocs.io/en/stable/user-guide/multiple_sources/)
- Git tag ranges can use an application prefix in current Argo CD. Case 61 uses the documented `tagPrefix` field. The installed Argo CD CRD must support it. [Tracking strategies](https://argo-cd.readthedocs.io/en/stable/user-guide/tracking_strategies/), [Application CRD](https://raw.githubusercontent.com/argoproj/argo-cd/master/manifests/crds/application-crd.yaml)
- SCM-provider discovery scans organizations. Pull-request generators expose the PR head SHA. Cases 62-63 use these inputs. [SCM provider](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-SCM-Provider/), [pull-request generator](https://argo-cd.readthedocs.io/en/stable/operator-manual/applicationset/Generators-Pull-Request/)

### Inferences

- The maintained documentation and examples justify broad pattern coverage. They do not establish percentages or rank generator adoption.
- Repository access boundaries cannot be recreated inside one public repository. Cases 02-04 test the directory content and source routing, with that limitation stated in each case.

### Gaps

- No reliable adoption survey was found for these individual layout and generator patterns.

## What does Radar actually do?

### Takeaway

The predicted results for these 23 cases are 17 supported, five refusals, and one unsure planner error. No wrong edit was established in this slice. These are code predictions with local workload validation, not live pull-request trials.

### Cited findings


### Inferences

- Creating an Application through an ApplicationSet does not itself block editing its plain workload source. Cases 14 and 16 assume Radar can read the generated Application and complete live membership. Missing membership can add possible-reader scope confirmation.
- The same literal-source proof applies to Applications in a team namespace after Argo CD accepts the Application. Case 17 still needs namespace and project configuration.

### Gaps

- Live ownership evidence, admission policies, quota state, and user permissions can change the offered route. The case notes state the baseline assumptions.
- No live Argo CD or Radar service was started by this research slice. A standalone locator check does not exercise service authentication or revision resolution.

## What was verified, and what still needs setup?

### Takeaway

Every case has locally valid workload YAML and exactly one Deployment with the requested image, one replica, a 16Mi memory request, and a 64Mi limit. Publication and controller prerequisites are separate from that check.

### Cited findings

- Case 01 was built with `kustomize build`; the other workload sources were parsed as plain YAML using the commands recorded in their `case.yaml` files.
- ApplicationSet samples in `generated-application.yaml` show derived output for inspection. They are outside workload source paths and are not additional Applications to install.
- A read-only upstream ref query found tag `v1`, peeled to commit `87574024b437e74fcec2c66dba5c1eea16aae82d`. Case 18 uses that real tag. Case 19 uses existing commit `1aae77ad67138686544a33f739fa7b6edca2120a`. Both predate the new catalog, so their source paths are unavailable until later publication and repinning. [Public test repository](https://github.com/hisco/argotests)

### Inferences

- A local render check proves fixture content. It cannot prove that the public repository already serves uncommitted files.

### Gaps

- Case 05 needs a `production` branch containing the catalog. No branch was created.
- Cases 18-19 intentionally use real historical refs for the service refusal. To deploy their workloads, publish the fixtures and update the tag or SHA first.
- Case 14 needs one registered cluster matching its selector. No cluster credentials are included.
- Case 17 needs Argo CD and project namespace configuration. The catalog uses the required `default` project, although the official namespace guide recommends a restricted project for tenants.
- Case 61 needs matching published app-prefixed semver tags. Its local workload is valid, but the public repository does not yet have the required release tags containing this tree.
- Case 62 discovers the real public `argoproj/argo-cd` repository and uses its name to select central catalog configuration. It deploys podinfo from this test repository, not Argo CD's source tree. Anonymous discovery is rate limited and was not executed through an ApplicationSet controller.
- Case 63 needs an open labelled preview PR containing this fixture. Its derived sample uses historical PR 31 and its observed real head commit. That commit predates this catalog. No PR was created or labelled.
- Repository per team and ambiguous branch/tag names remain researched layout/ref considerations rather than separate fixtures in this slice. A single public repository cannot reproduce team repository access boundaries. Ambiguous names need matching published refs before controller-resolution differences can be exercised. Their generic guidance is [repository structure](https://fluxcd.io/flux/guides/repository-structure/) and [tracking strategies](https://argo-cd.readthedocs.io/en/stable/user-guide/tracking_strategies/).
