from setuptools import setup
import pathlib
from src.socketsc.version import version

ROOT_DIR = pathlib.Path(__file__).parent

packages = ['socketsc']
long_description = (ROOT_DIR / "README.rst").read_text()

setup(
    name="socketsc",
    version=version,
    description="Simple socket library for client/server with events management.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="server client socket event tcp",
    license="MIT",
    author="Dan5py",
    python_requires=">=3.8.0",
    url="https://gitlab.com/dan5py/socketsc",
    package_dir={"": "src"},
    include_package_data=True,
    requires=['wheel'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
