#!/usr/bin/env python3
"""Run the render command in each case and check the resulting workload."""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import yaml


ROOT = Path(__file__).resolve().parent.parent
IMAGE = "ghcr.io/stefanprodan/podinfo:6.7.1"


def resources(documents):
    for document in documents:
        if not isinstance(document, dict):
            continue
        if document.get("kind") == "List":
            yield from resources(document.get("items", []))
        else:
            yield document


def check_case(path):
    case = yaml.safe_load(path.read_text())
    result = {"case": case["id"], "command": case["render_check"]["command"]}
    try:
        sample = path.parent / "generated-application.yaml"
        entry = sample if sample.exists() else ROOT / "catalog" / "argocd" / (path.parent.name + ".yaml")
        app = yaml.safe_load(entry.read_text())
        spec = app["spec"]["template"]["spec"] if app["kind"] == "ApplicationSet" else app["spec"]
        destination = spec["destination"]["namespace"]
        assert destination == "cat-" + path.parent.name[:2], "Application destination namespace differs from case namespace."
        with tempfile.TemporaryDirectory(prefix="catalog-render-") as temporary:
            environment = os.environ.copy()
            for key, name in [("HELM_CACHE_HOME", "cache"), ("HELM_CONFIG_HOME", "config"), ("HELM_DATA_HOME", "data")]:
                location = Path(temporary) / name
                location.mkdir()
                environment[key] = str(location)
            (Path(temporary) / "cache" / "repository").mkdir()
            process = subprocess.run(
                result["command"], shell=True, cwd=ROOT, capture_output=True,
                text=True, timeout=90, env=environment,
            )
        if process.returncode:
            result.update(status="failed", error="Render command exited unsuccessfully.")
            return result
        objects = list(resources(yaml.safe_load_all(process.stdout)))
        deployments = [o for o in objects if o.get("kind") == "Deployment"]
        if not deployments:
            services = [o for o in objects if o.get("apiVersion", "").startswith("serving.knative.dev/") and o.get("kind") == "Service"]
            if len(services) == 1:
                container = services[0]["spec"]["template"]["spec"]["containers"][0]
                assert container["image"] == IMAGE
                assert container["resources"]["requests"]["memory"] == "16Mi"
                assert container["resources"]["limits"]["memory"] == "64Mi"
                result.update(status="runtime-exception", observation="Knative Service sets 64Mi. Its controller creates the Deployment at runtime.")
                return result
            raise AssertionError("Expected exactly one Deployment.")
        assert len(deployments) == 1, "Expected exactly one Deployment."
        deployment = deployments[0]
        assert deployment["metadata"]["name"] == path.parent.name[3:], "Deployment name differs from case short ID."
        assert deployment["spec"]["replicas"] == 1, "Expected one replica."
        namespace = deployment["metadata"].get("namespace", destination)
        assert namespace == "cat-" + path.parent.name[:2], "Deployment namespace differs from case namespace."
        containers = deployment["spec"]["template"]["spec"]["containers"]
        assert len(containers) == 1, "Expected one application container."
        container = containers[0]
        assert container["image"] == IMAGE, "Unexpected image."
        assert container["resources"]["requests"]["memory"] == "16Mi", "Expected memory request 16Mi."
        limit = container["resources"].get("limits", {}).get("memory")
        if limit is None:
            defaults = [entry.get("default", {}).get("memory") for o in objects if o.get("kind") == "LimitRange" for entry in o["spec"]["limits"] if entry.get("type") == "Container"]
            assert "64Mi" in defaults, "Missing limit without a LimitRange default of 64Mi."
            result.update(status="runtime-exception", observation="Deployment omits the limit. LimitRange supplies 64Mi to admitted Pods.")
        else:
            assert limit == "64Mi", "Expected memory limit 64Mi."
            result.update(status="passed", deployment=deployment["metadata"]["name"], namespace=namespace, container=container["name"], memory_request="16Mi", memory_limit=limit)
    except (AssertionError, KeyError, ValueError, yaml.YAMLError, subprocess.TimeoutExpired) as error:
        result.update(status="failed", error=str(error))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a JSON report.")
    arguments = parser.parse_args()
    paths = sorted((ROOT / "catalog").glob("[0-9][0-9]-*/case.yaml"))
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check_case, paths))
    report = {"scope": "Local rendering. No live Argo CD, admission, or controller reconciliation was run.", "results": results}
    if arguments.output:
        arguments.output.write_text(json.dumps(report, indent=2) + "\n")
    for result in results:
        print(result["case"], result["status"], result.get("error", ""))
    return int(any(result["status"] == "failed" for result in results))


if __name__ == "__main__":
    sys.exit(main())
