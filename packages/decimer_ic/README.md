# DECIMER Image Classifier
[![License](https://img.shields.io/badge/License-MIT%202.0-blue.svg)](https://opensource.org/licenses/MIt)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-blue.svg)](https://GitHub.com/iagea/DECIMER-Image-Classifier/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/iagea/DECIMER-Image-Classifier.svg)](https://GitHub.com/iagea/DECIMER-Image-Classifier/issues/)
[![GitHub contributors](https://img.shields.io/github/contributors/iagea/DECIMER-Image-Classifier.svg)](https://GitHub.com/iagea/DECIMER-Image-Classifier/graphs/contributors/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6670746.svg)](https://doi.org/10.5281/zenodo.6670746)


- This model aims to classify whether or not an image is a chemical structure. It was built using EfficientNetB0 as a base model, using transfer learning and fine-tuning it.

- It gives a prediction between 0 and 1 where 0 means it is a chemical structure and 1 means it is not. The data used to build the model is available in Zenodo. 


## Changed README for adapted standalone version
Most of original README deleted (since not relevant) for this standalone version. Check the original git repo for other details.<br>
The modelbuilding folder and the testing was removed here, though the modebuilding still works if one wanted to give that a go (see the original repo for details).

## Purpose
This standalone version was made to simplify setup together with DECIMER Image Transformer due to potential install incompatibilities encountered when used together.

## Installation
Intended to work with installation of DECIMER-V2, i.e. DECIMER-Image-Transformer, see github: https://github.com/Iagea/DECIMER-Image-Classifier/tree/main.<br>
This here will is installed `python setup.py install`<br>
Since this particular package is mainly intended for used with Image Transformer and a server API, this and dependencies are taken care of by the top level installation.

## Adapted by: [DocMinus](https://github.com/DocMinus)
December 2024

## Version
changed from 1.0.1 to 1.0.2 for this adaption.

## Original Author: [M. Isabel Agea](https://iagea.github.io)
Shout-out to original author of this classifier.

## Model construction
For this standalone installation, model construction was removed (though it works if one wants to test, check the orignal github for this)


