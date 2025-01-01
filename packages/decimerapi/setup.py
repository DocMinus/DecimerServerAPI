import os

from setuptools import find_packages, setup

setup_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(setup_dir, "README.md"), "r") as fh:
    long_description = fh.read()

setup(
    name="decimerapi",
    version="0.5.0",
    author="Alexander Minidis",
    author_email="your_email@example.com",
    description="A wrapper module for decimer as used by API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests",
    ],
)
