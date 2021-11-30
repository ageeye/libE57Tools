# libE57Tools
Test library to import E57 files to FreeCAD

Compiling
===

```
git clone --recurse-submodules https://github.com/ageeye/libE57Tools.git
cd libE57Tools
mkdir build && cd build
XERCES_ROOT="/usr/local/Cellar/xerces-c/3.2.2/" cmake ..
cd libE57Format
make
cd ..
make
```

Licens
===

This project as a whole is licensed under the BSL-1.0 license.
