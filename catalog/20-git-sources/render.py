"""Print the independent Git sources as one YAML stream."""

from pathlib import Path
import sys

import yaml

case = Path(__file__).resolve().parent
documents = []
for source in [case / "apps" / "checkout", case / "shared"]:
    for manifest in sorted(source.glob("*.yaml")):
        documents.extend(yaml.safe_load_all(manifest.read_text()))
yaml.safe_dump_all(documents, sys.stdout, sort_keys=False, explicit_start=True)
