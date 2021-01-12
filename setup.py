#!/usr/bin/env python3
from setuptools import setup
from nudatus import get_version


with open("README.rst") as f:
    readme = f.read()
with open("CHANGES.rst") as f:
    changes = f.read()


extras_require = {
    "tests": [
        "pytest>=4.6",
        "pytest-cov",
        "pytest-random-order>=1.0.0",
        "pytest-faulthandler",
        "coverage",
        "black",
    ],
    "package": [
        # Wheel building and PyPI uploading
        "wheel",
        "twine",
    ],
}

extras_require["dev"] = extras_require["tests"] + extras_require["package"]

extras_require["all"] = list(
    {req for extra, reqs in extras_require.items() for req in reqs}
)

setup(
    name="nudatus",
    version=get_version(),
    description="Strip comments from scripts, intended for use with "
    "MicroPython and other storage constrained "
    "environments",
    long_description=readme + "\n\n" + changes,
    author="Zander Brown",
    url="https://github.com/zanderbrown/nudatus",
    py_modules=[
        "nudatus",
    ],
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.5",
    ],
    python_requires=">=3.5",
    extras_require=extras_require,
    entry_points={
        "console_scripts": ["nudatus=nudatus:main"],
    },
)
