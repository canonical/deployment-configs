from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="konf",
    version="0.1.0",
    install_requires=requirements,
    scripts=["konf.py"]
)
