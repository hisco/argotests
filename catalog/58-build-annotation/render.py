from pathlib import Path
import copy, subprocess, tempfile, shutil, yaml
case = Path(__file__).resolve().parent
root = case.parent.parent
app = yaml.safe_load((case.parent / 'argocd' / (case.name + '.yaml')).read_text())
source = root / app['spec']['source']['path']
opts = copy.deepcopy(app['spec']['source']['kustomize'])
opts.pop('version', None)
envsubst = opts.pop('commonAnnotationsEnvsubst', False)
if envsubst:
    for key, value in opts.get('commonAnnotations', {}).items():
        opts['commonAnnotations'][key] = value.replace('${ARGOCD_APP_NAME}', app['metadata']['name']).replace('$ARGOCD_APP_NAME', app['metadata']['name'])
with tempfile.TemporaryDirectory() as directory:
    target = Path(directory) / 'checkout'
    shutil.copytree(source, target)
    path = target / 'kustomization.yaml'
    current = yaml.safe_load(path.read_text())
    for key, value in opts.items():
        if key == 'patches':
            current.setdefault(key, []).extend(value)
        else:
            current[key] = value
    path.write_text(yaml.safe_dump(current, sort_keys=False))
    subprocess.run(['kustomize', 'build', str(target)], check=True)
