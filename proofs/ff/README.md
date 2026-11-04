Free-field fixtures: values other than memory, image and replicas, set once in Git.
plain/ is plain manifests, kinds/ holds an Ingress, a CronJob and an HPA, helm/ is a local chart
with the values in values.yaml, overlay/ is a Kustomize base with a prod overlay that patches some values.
