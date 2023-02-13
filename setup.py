import re
from pathlib import Path

from setuptools import setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

path = Path(__file__).parent / "mokie" / "__init__.py"
version = re.search(r"\d[.]\d[.]\d", path.read_text())

if not version:
    raise RuntimeError('version is not set')

version = version[0]
packages = ["mokie", "mokie.impl", "mokie.models"]


setup(
    name="Mokie",
    author="SawshaDev",
    version=version,
    packages=packages,
    license="MIT",
    description="A revolt api wrapper, what more is there to say?",
    install_requires=requirements,
    python_requires=">=3.8.0",
)
