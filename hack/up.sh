#!/bin/bash
# A kind cluster running Argo CD, pointed at this repository.
#
# Argo is given the two kustomize build options a chart-inflating kustomization
# needs, because without them a converted application does not render and the
# failure looks like a bad conversion rather than a missing setting.
set -e
export KUBECONFIG=${KUBECONFIG:-/tmp/kc-argotests.yaml}
kind create cluster --name argotests --kubeconfig "$KUBECONFIG"
kubectl create namespace argocd
# Server-side: the ApplicationSet CRD is too large for the annotation kubectl
# apply writes.
kubectl apply -n argocd --server-side=true -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl -n argocd patch cm argocd-cm --type merge \
  -p '{"data":{"kustomize.buildOptions":"--enable-helm --load-restrictor LoadRestrictionsNone"}}'
kubectl -n argocd rollout restart deploy/argocd-repo-server
kubectl -n argocd rollout status deploy/argocd-repo-server --timeout=300s
kubectl -n argocd rollout status statefulset/argocd-application-controller --timeout=300s
kubectl apply -f "$(dirname "$0")/../argocd/"
echo "Applied. Watch with: kubectl -n argocd get applications -w"
