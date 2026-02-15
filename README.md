# miru-core

Python bindings for [Miru](https://miru.re). (`import miru`)

## Install (pip)

    pip install miru-core

## Some tips during development

To build and test your own wheel, do something along the following lines:

```
set MIRU_VERSION=16.0.1-dev.7 # from C:\src\miru\build\tmp-windows\miru-version.h
set MIRU_EXTENSION=C:\src\miru\build\miru-windows\x64-Release\lib\python3.10\site-packages\_miru.pyd
cd C:\src\miru\miru-core\
pip wheel .
pip uninstall miru-core
pip install miru_core-16.0.1.dev7-cp39-abi3-win_amd64.whl
python -c "import miru; print(miru.__version__)"
```
