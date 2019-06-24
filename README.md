# QuteMap

[![MIT license](https://img.shields.io/badge/License-GPLv3-brightgreen.svg)](https://github.com/eyllanesc/QuteMap/blob/master/LICENSE)
[![Tagged Release](https://img.shields.io/badge/release-v0-blue.svg?longCache=true)](CHANGELOG.md)
[![Pypi Status](https://img.shields.io/pypi/v/QuteMap.svg)](https://pypi.python.org/pypi/QuteMap)
[![Development Status](https://img.shields.io/badge/status-planning-lightgrey.svg?longCache=true)](ROADMAP.md)
[![Build Status](https://img.shields.io/travis/eyllanesc/QuteMap.svg)](https://travis-ci.org/eyllanesc/QuteMap)
[![PyUp Status](https://pyup.io/repos/github/eyllanesc/QuteMap/shield.svg)](https://pyup.io/repos/github/eyllanesc/QuteMap/)
[![Documentation Status](https://readthedocs.org/projects/qutemap/badge/?version=latest)](https://qutemap.readthedocs.io/en/latest/?badge=latest)

Maps using Qt WebEngine and Qt WebChannel using PyQt5/PySide2

- Documentation: https://QuteMap.readthedocs.io.


## Features

- Programatically centering, zooming and manipulate markers
- Flexible marker properties (ie. draggable, icon, title…)
- Emits signals on user actions: dragged markers, pans or zooms
- Easy to add map plugins, currently supports googlemaps and osm


## Requirements

- [Jinja2](http://jinja.pocoo.org/)
- [Click](https://palletsprojects.com/p/click/)
- [PyYAML](https://github.com/yaml/pyyaml)
- [dataclasses](https://github.com/ericvsmith/dataclasses)  (for Python 3.6)

**Backends:**

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) + [PyQtWebEngine](https://www.riverbankcomputing.com/software/pyqtwebengine/intro) or
- [PySide2](https://www.pyside.org/)

## Installation

To install QuteMap, run this command in your terminal:

```console
$ pip install QuteMap
```

Or from source code:

```console
$ git clone git://github.com/eyllanesc/QuteMap
$ python setup.py install
``` 
## Usage

## Development

See [CONTRIBUTING](https://github.com/eyllanesc/QuteMap/blob/master/CONTRIBUTING.rst)

### Future

See [ROADMAP](https://github.com/eyllanesc/QuteMap/blob/master/ROADMAP.md)

### History

See [HISTORY](https://github.com/eyllanesc/QuteMap/blob/master/HISTORY.rst)

### Community

See [CODE OF CONDUCT](https://github.com/eyllanesc/QuteMap/blob/master/CODE_OF_CONDUCT.md)

## License

Free software: [GNU General Public License v3](https://github.com/eyllanesc/QuteMap/blob/master/LICENSE)


## Credits

- This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) project template.
- This project was initially created by [cookiecutter-git](https://github.com/NathanUrwin/cookiecutter-git).
- This project use [Qt.py](https://github.com/mottosso/Qt.py).
