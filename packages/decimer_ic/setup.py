#!/usr/bin/env python
import setuptools
import os


setup_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(setup_dir, "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="decimer_image_classifier",
    version="1.0.3",
    author="Isabel Agea",
    author_email="Maria.Isabel.Agea.Lorente@vscht.cz",
    description="DECIMER Image Classifier based on EfficientNetB0 for structure recognition. Adapted setup for standalone use.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Iagea/DECIMER-Image-Classifier",
    packages=setuptools.find_packages(),
    license="MIT",
    package_data={"decimer_image_classifier": ["*.*", "model/*.*", "model/*/*.*"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "decimer",
    ],
)
