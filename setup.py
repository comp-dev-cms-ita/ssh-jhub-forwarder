#!/usr/bin/env python
# Copyright (c) 2021 dciangot
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


from __future__ import print_function

import os
import sys

from setuptools import setup
from glob import glob

pjoin = os.path.join
here = os.path.abspath(os.path.dirname(__file__))

# Get the current package version.
version_ns = {}
with open(pjoin(here, "version.py")) as f:
    exec(f.read(), {}, version_ns)

with open(pjoin(here, "README.md"), encoding="utf-8") as f:
    long_desc = f.read()

setup_args = dict(
    name="ssh-jhub-forwarder",
    packages=["ssh_jhub_forwarder"],
    scripts=["scripts/ssh-jhub-forwarder.py","scripts/ssh-jhub-start.sh","scripts/ssh-jhub-listener.py", "scripts/ssh-jhub-listener-start.sh"],
    version=version_ns["__version__"],
    description="""SSH server to forward connection on remote cluster with JupyterHUB token authentication""",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="D. Ciangottini, D. Spiga, M. Tracolli,",
    author_email="dciangot@cern.ch",
    url="http://github.com/comp-dev-cms-ita/ssh-jhub-forwarder",
    license="MIT",
    platforms="Linux",
    python_requires="~=3.6",
    keywords=["Interactive", "Dask", "Distributed"],
    include_package_data=True,
)

# setuptools requirements
if "setuptools" in sys.modules:
    setup_args["install_requires"] = install_requires = []
    with open("requirements.txt") as f:
        for line in f.readlines():
            req = line.strip()
            if not req or req.startswith(("-e", "#")):
                continue
            install_requires.append(req)


def main():
    setup(**setup_args)


if __name__ == "__main__":
    main()
