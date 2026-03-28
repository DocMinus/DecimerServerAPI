# FAQ

## Why this version?

The original DECIMER repositories had several issues:

1. **Dependency hell** - Installation was problematic due to complex dependencies across different systems
2. **No self-deployable server** - No server version was available
3. **Slow startup** - Loading models on each script invocation was time-consuming

This version solves these by:
- Providing a Docker option for robust, environment-independent deployment
- Server-based architecture with one-time model loading
- Integrated image classifier to filter out non-molecule images early

## Important Caveats

> **Warning:** Although the classifier can be overridden, it is not recommended. If you have non-molecule images, the system might crash due to the decimer image-to-SMILES implementation.

> **Note:** First-time startup might take a few minutes due to model download (depends on connection speed; happens only once).

> **Note:** Initial recognition calls take time, but batch submissions are much faster after the first call.

## Uninstalling

To uninstall, remove the application folder and Python environment, then delete the `.data` folder in your home directory where Decimer stores its models.
