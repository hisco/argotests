#!/bin/sh
set -eu
limit="${ARGOCD_ENV_MEMORY_LIMIT:-64Mi}"
case "$limit" in
  *[!0-9A-Za-z]*) echo "Memory limit must be a Kubernetes quantity without punctuation." >&2; exit 1 ;;
esac
sed "s/MEMORY_LIMIT/$limit/g" deployment.yaml.in
