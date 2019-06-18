import pyqtgraph as pg
from pyqtgraph.Qt import QtGui

class previewPlot(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.setupUi()

    def setupUi(self):
        layout = QtGui.QVBoxLayout()
        self.imageView = pg.ImageView()
        layout.addWidget(self.imageView)
        self.setLayout(layout)
