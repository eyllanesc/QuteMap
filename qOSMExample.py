#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qOSM import *

if __name__ == '__main__':
    import sys


    def goCoords():
        def resetError():
            coordsEdit.setStyleSheet('')

        try:
            latitude, longitude = coordsEdit.text().split(",")
        except ValueError:
            coordsEdit.setStyleSheet("color: red;")
            QtCore.QTimer.singleShot(500, resetError)
        else:
            map.centerAt(latitude, longitude)
            # map.moveMarker("MyDragableMark", latitude, longitude)


    def onMarkerMoved(key, latitude, longitude):
        print("Moved!!", key, latitude, longitude)
        coordsEdit.setText("{}, {}".format(latitude, longitude))


    def onMarkerRClick(key):
        print("RClick on ", key)
        # map.setMarkerOptions(key, draggable=False)


    def onMarkerLClick(key):
        print("LClick on ", key)


    def onMarkerDClick(key):
        print("DClick on ", key)
        # map.setMarkerOptions(key, draggable=True)


    def onMapMoved(latitude, longitude):
        print("Moved to ", latitude, longitude)


    def onMapRClick(latitude, longitude):
        print("RClick on ", latitude, longitude)


    def onMapLClick(latitude, longitude):
        print("LClick on ", latitude, longitude)


    def onMapDClick(latitude, longitude):
        print("DClick on ", latitude, longitude)


    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QDialog()
    h = QtWidgets.QVBoxLayout(w)
    l = QtWidgets.QFormLayout()
    h.addLayout(l)
    coordsEdit = QtWidgets.QLineEdit()
    l.addRow('Coords:', coordsEdit)
    coordsEdit.editingFinished.connect(goCoords)
    map = QOSM(w)
    map.mapMoved.connect(onMapMoved)
    map.markerMoved.connect(onMarkerMoved)
    map.mapClicked.connect(onMapLClick)
    map.mapDoubleClicked.connect(onMapDClick)
    map.mapRightClicked.connect(onMapRClick)
    map.markerClicked.connect(onMarkerLClick)
    map.markerDoubleClicked.connect(onMarkerDClick)
    map.markerRightClicked.connect(onMarkerRClick)
    h.addWidget(map)
    map.setSizePolicy(
        QtWidgets.QSizePolicy.MinimumExpanding,
        QtWidgets.QSizePolicy.MinimumExpanding)
    w.show()

    map.waitUntilReady()

    map.centerAt(-12.0464, -77.0428)
    map.setZoom(12)
    # Many icons at: https://sites.google.com/site/gmapsdevelopment/
    coords = map.center()
    map.addMarker("MyDragableMark", *coords, **dict(
        icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png",
        draggable=True,
        title="Move me MyDragableMark!"
    ))

    coords = coords[0] + 0.1, coords[1] + 0.1
    map.addMarker("MyDragableMark2", *coords, **dict(
        icon="http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png",
        draggable=True,
        title="Move me MyDragableMark2"
    ))

    sys.exit(app.exec_())
