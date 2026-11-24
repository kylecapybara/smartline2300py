# pysmartline

`pysmartline` is a Python package for communicating with and collecting data from Knauer Smartline detector devices. The Knauer Smartline 2300 detector series requires either an analogue signal measurement (no command sending ability) or ancient, proprietary software. No open-source tools exist for direct RS-232 communication, and information shared by customer support is not only incomplete, but also incorrect. This package provides a documented, scriptable interface enabling automated workflows and reproducible data acquisition in research laboratories for applications such as chromatographic separations on larger-than-HPLC scale and residence time distribution measurement.

NOTE: use a null modem cable!


## Installation

From the project root, install in editable mode:

```bash
pip install -e .
```

Or install from a local source checkout:

```bash
pip install .
```
