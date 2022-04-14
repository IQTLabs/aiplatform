import hashlib
import os
from pathlib import Path
import shutil
import subprocess

import requests
import yaml

CHUNK_SIZE = 2 ** 13

container_path = Path("mlflow")
resources_path = container_path / "resources"

os.makedirs(resources_path, exist_ok=True)

with open(container_path / "hardening_manifest.yaml", "r") as f:
    hm = yaml.load(f, yaml.Loader)


for resource in hm['resources']:
    resource_path = resources_path / resource['filename']
    if not resource_path.exists():
        h = hashlib.new(resource['validation']['type'])
        with requests.get(resource['url'], stream=True) as r:
            r.raise_for_status()
            with open(resource_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
                    h.update(chunk)
        print(h.hexdigest())
        print(resource['validation']['value'])


dockerfile_path = resources_path / "Dockerfile"
if not dockerfile_path.exists():
    shutil.copy(container_path / "Dockerfile", dockerfile_path)

subprocess.run(["docker", "build", "--tag", f"{hm['name']}:{hm['tags'][0]}", "."], cwd=resources_path)
