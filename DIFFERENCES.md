# Differences from Original Decimer Packages

This document explains the changes made compared to the original [DECIMER V2](https://github.com/Kohulan/DECIMER-Image_Transformer) and [DECIMER Image Classifier](https://github.com/Iagea/DECIMER-Image-Classifier) packages.

## Changes vs. Decimer Transformer Package

- **Mac Silicon Tensorflow support** - Installation handles Mac M1/M2/M3 GPU acceleration via `tensorflow-macos` and `tensorflow-metal` (local install only, not Docker)
- **Server-based API** - The server version uses JSON calls; the standalone version overrides the original `predict_smiles()`
- **Python API provided** - Easy integration with existing Python projects
- **Note:** You can still use the original `predict_smiles()` function by installing the decimer packages directly

## Changes vs. Classifier Package

- **Adjusted threshold** - Uses classifier score < 0.3 instead of true/false readout, allowing reaction schemes to be classified as structures
- **Reaction scheme support** - The original classifier wasn't designed for reaction schemes, but this threshold adjustment makes it work
- **Modified keras calls** - Changed to `tf.keras` instead of standalone `keras`
- **Removed image saving** - Removed unnecessary `save_image` command

To adjust the threshold, edit `IC_THRESHOLD` in `decimer_server.py`.
