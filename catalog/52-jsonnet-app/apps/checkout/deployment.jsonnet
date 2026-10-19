local memory = std.extVar("memory");
{
  "apiVersion": "apps/v1",
  "kind": "Deployment",
  "metadata": {
    "name": "jsonnet-app",
    "namespace": "cat-52",
    "labels": {
      "app.kubernetes.io/name": "jsonnet-app",
      "app.kubernetes.io/part-of": "checkout"
    }
  },
  "spec": {
    "replicas": 1,
    "selector": {
      "matchLabels": {
        "app.kubernetes.io/name": "jsonnet-app"
      }
    },
    "template": {
      "metadata": {
        "labels": {
          "app.kubernetes.io/name": "jsonnet-app"
        }
      },
      "spec": {
        "containers": [
          {
            "name": "podinfo",
            "image": "ghcr.io/stefanprodan/podinfo:6.7.1",
            "command": [
              "./podinfo"
            ],
            "ports": [
              {
                "containerPort": 9898,
                "name": "http"
              }
            ],
            "resources": {
              "requests": {
                "memory": "16Mi"
              },
              "limits": {
                "memory": memory
              }
            }
          }
        ]
      }
    }
  }
}
