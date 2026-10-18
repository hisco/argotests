# platform

A small GitOps repo laid out the way a real company one tends to be. It is a
test fixture for Radar's "fix memory limit in Git" flow, so it has the usual
mess: Helm charts with per-cluster values files, Kustomize overlays, addons,
and ApplicationSets that discover everything from folder names.

It runs on a kind cluster with Argo CD installed. Two cluster names exist,
`kind-e2e` and `kind-e2e-2`. Both point at the local cluster, so you can run
either one or both on a single kind cluster.

## Layout

```
argocd/
  cluster-admin-project.yaml     bootstrap AppProject, applied by hand once
  bootstrap/
    root-app.yaml                app of apps, applied by hand once
    auto-provision-clusters/     one AppProject app per cluster + shared components
    shared-components/           addons + workloads AppProjects and discovery ApplicationSets
  cluster-config/<cluster>/      config.json (cluster facts) + appproject.yaml
  addons/utilities/<addon>/      kustomize: base/ + overlays/<cluster>/
environments/<env>.yaml          which cluster each environment lives on
deployment-repo/<app>/           one folder per app
  argocd/<env>.yaml              the Application for that env
```

## Bootstrap order

An ApplicationSet whose AppProject doesn't exist yet fails and is only retried
three minutes later, so sync waves put every AppProject first:

- `auto-provision-clusters/`: the cluster AppProjects ApplicationSet at wave -1,
  `shared-components` at wave 1.
- `shared-components/`: the addons and workloads AppProjects at wave -1, the
  two discovery ApplicationSets at wave 1.

## Apps

| App | Kind | Where the memory limit lives |
|---|---|---|
| `checkout` | Helm chart | `chart/values-<cluster>.yaml` (overrides `chart/values.yaml`) |
| `worker` | Helm chart, crashes on purpose | `chart/values-<cluster>.yaml` (overrides `chart/values.yaml`) |
| `catalog` | Kustomize | `overlays/<cluster>/limits-patch.yaml` |

`worker` runs podinfo with `--stress-memory=200`, which loads 200 MB into
memory. Its limit is 64Mi on `kind-e2e` and 96Mi on `kind-e2e-2`, so it gets
OOM-killed on both. The fix is to raise `resources.limits.memory` in
`deployment-repo/worker/chart/values-kind-e2e.yaml` (or the `-2` file).

## How discovery works

- A folder in `argocd/cluster-config/` is a cluster. Remove the folder to drop it.
- An addon is on for a cluster when `addons/**/<cluster>/*-appset.yaml` exists.
- An environment is a file in `environments/`. It names the cluster it runs on.
  Every `deployment-repo/<app>/argocd/<env>.yaml` is then deployed to it.

## Use it

Install Argo CD on the kind cluster, then:

```
kubectl apply -f platform/argocd/cluster-admin-project.yaml
kubectl apply -f platform/argocd/bootstrap/root-app.yaml
```

Everything points at `https://github.com/hisco/argotests.git`, branch `main`,
so these paths only work once this folder is on `main`.

Requests add up to 120m CPU and 128Mi per cluster, so 240m and 256Mi with both clusters running.
