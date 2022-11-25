from setuptools import setup, find_packages

PACKAGE_NAME = "socketsc"
VERSION = "1.0.0"
DESCRIPTION = "Simple socket library with events management."
KEYWORDS = "Server Client Socket Sockets Event TCP"
URL = "https://gitlab.com/dan5py/socketsc"
AUTHOR = "Dan5py"
LICENSE = "Apache License 2.0"
REQUIRES_PYTHON = ">=3.8.0"
EXTRAS = {}

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

# with open("requirements.txt", "r") as f:
#     requirements = [line.strip() for line in f.readlines()]
requirements = []

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=KEYWORDS,
    license=LICENSE,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(include=f"{PACKAGE_NAME}.*"),
    install_requires=requirements,
    extras_require=EXTRAS,
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
