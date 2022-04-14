#!/usr/bin/env python

from argparse import ArgumentParser
import hashlib
import logging
import os
from pathlib import Path
import shutil
import subprocess

import requests
import yaml

# Logging configuration
root = logging.getLogger()
if not root.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    root.addHandler(ch)

logger = logging.getLogger("build")
logger.setLevel(logging.INFO)

# Build parameters
CONTAINER_NAMES = ["mlflow"]
CHUNK_SIZE = 2**13


def build_image(container_name, force=False, clean=False):
    """ """
    # Load the hardening manifest
    logger.info(f"Building image for container {container_name}")
    container_path = Path(container_name)
    with open(container_path / "hardening_manifest.yaml", "r") as f:
        hm = yaml.load(f, yaml.Loader)

    # Downoad the all resources in the manifest
    resources_path = container_path / "resources"
    os.makedirs(resources_path, exist_ok=True)
    for resource in hm["resources"]:
        resource_path = resources_path / resource["filename"]
        if not resource_path.exists() or force:
            logger.info(f"Downloading {resource['filename']}")

            # Download and hash
            h = hashlib.new(resource["validation"]["type"])
            with requests.get(resource["url"], stream=True) as r:
                r.raise_for_status()
                with open(resource_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
                        f.write(chunk)
                        h.update(chunk)

            # Ensure the hashes agree
            if h.hexdigest() != resource["validation"]["value"]:
                logger.error(f"Hashes do not agree for {resource['filename']}")

    # Build the Dockerfile
    dockerfile_path = resources_path / "Dockerfile"
    if not dockerfile_path.exists() or force:
        shutil.copy(container_path / "Dockerfile", dockerfile_path)
    image = f"{hm['name']}:{hm['tags'][0]}"
    logger.info(f"Building image {image}")
    subprocess.run(
        ["docker", "build", "--tag", image, "."],
        cwd=resources_path,
    )

    # Optionally clean up
    if clean:
        logger.info(f"Cleaning up")
        shutil.rmtree(resources_path)


if __name__ == "__main__":
    # Optionally force downloads or copies, or clean up
    parser = ArgumentParser(description="Build docker images")
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="force file downloads or copies",
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="remove file downloads and copies",
    )
    args = parser.parse_args()

    # Build image for each container name
    for container_name in CONTAINER_NAMES:
        build_image(container_name, force=args.force, clean=args.clean)
