import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="anyskin",
    version="1.0.0",
    author="Raunaq Bhirangi",
    author_email="raunaqbhirangi@nyu.edu",
    description="Python library for interfacing with an AnySkin sensor",
    long_description=read("README.md"),
    packages=find_packages(),
    install_requires=["numpy>=1.24", "pyserial>=3.5", "pygame>=2.6.0"],
    python_requires=">=3.8",
    url="https://github.com/raunaqbhirangi/anyskin.git",
    entry_points={
        "console_scripts": [
            "anyskin_viz=anyskin.visualizations.anyskin_viz:default_viz"
        ],
    },
)
