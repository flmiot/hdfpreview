import os
import sys

DEV = True

if DEV:
    os.system("pyrcc5 development/resources.qrc -o resources_rc.py")
    os.system("pyuic5 development/mainWindow.ui -o hdfpreview/ui/mainWindow.py")
    os.system("pyuic5 development/about.ui -o hdfpreview/ui/about.py")

from pyqtgraph.Qt import QtCore
import hdfpreview

if __name__ == '__main__':
    hdfpreview.app.exec_()
