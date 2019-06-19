from pyqtgraph.Qt import QtGui, QtCore
from hdfpreview.ui.mainWindow import Ui_MainWindow
from hdfpreview.ui.about import Ui_Dialog
from hdfpreview.logic import Dataset
import hdfpreview

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()
        self.aboutDialog = AboutDialog(self)


    @QtCore.pyqtSlot()
    def on_actionExit_triggered(self, *args, **kwargs):
        hdfpreview.app.quit()


    @QtCore.pyqtSlot()
    def on_actionPreviewDataSource_triggered(self, *args, **kwargs):
        try:
            currentItem = self.treeWidget.currentItem()
            path = currentItem.toolTip(0)
            data = hdfpreview.data.getData(path)
            self.central_plot.displayData(data, path)
        except:
            self.statusbar.showMessage("Error: No valid data source selected!")


    @QtCore.pyqtSlot()
    def on_actionLoadFiles_triggered(self, *args, **kwargs):

        # Read HDF5 filenames
        files = QtGui.QFileDialog.getOpenFileNames(self, 'Select HDF5 files')[0]
        hdfpreview.data = Dataset(files)

        # Update the file QListWidget
        self.listWidget.clear()
        self.listWidget.addItems(hdfpreview.data.get_filenames())

        # Update the data source QTreeWidget
        self.treeWidget.clear()
        data_sources = hdfpreview.data.get_data_tree()
        self.fillTreeWidget(data_sources, None)


    @QtCore.pyqtSlot()
    def on_actionAbout_Hdf5_preview_triggered(self, *args, **kwargs):
        if self.aboutDialog.isHidden():
            self.aboutDialog.show()


    def fillTreeWidget(self, dictionary, rootItem = None):
        if rootItem is None:
            rootItem = QtGui.QTreeWidgetItem(self.treeWidget)
            rootItem.setText(0, "Select a data source...")
            self.fillTreeWidget(dictionary, rootItem)
        else:
            for key, value in dictionary.items():
                item = QtGui.QTreeWidgetItem(rootItem)
                item.setText(0, key)
                if isinstance(value, dict):
                    self.fillTreeWidget(value, item)
                else:
                    item.setToolTip(0, value)


class AboutDialog(Ui_Dialog, QtGui.QDialog):
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.setupUi(self)
