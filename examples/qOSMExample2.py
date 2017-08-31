#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import qOSM
qOSM.use("PyQt4")

from qOSM.common import QOSM

if qOSM.get_backed() == "PyQt5":
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
elif qOSM.get_backed() == "PyQt4":
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *


def onTimeout(map, marker):
    lat, lng = map.positionMarker(marker)
    lat += 0.01*random.uniform(-1, 1)
    lng += 0.01*random.uniform(-1, 1)
    map.moveMarker(marker, lat, lng)
    map.centerAt(lat, lng)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    w = QDialog()
    w.setLayout(QVBoxLayout())

    map = QOSM(w)
    w.layout().addWidget(map)
    map.setSizePolicy(
        QSizePolicy.MinimumExpanding,
        QSizePolicy.MinimumExpanding)
    w.show()

    map.waitUntilReady()

    map.centerAt(-12.0464, -77.0428)
    map.setZoom(11)
    # Many icons at: https://sites.google.com/site/gmapsdevelopment/
    coords = map.center()
    p = map.addMarker("MyDragableMark", *coords, **dict(
        icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png",
        title="Move me MyDragableMark!"
    ))

    timer = QTimer()
    timer.timeout.connect(lambda: onTimeout(map, p))
    timer.start(100)

    sys.exit(app.exec_())
