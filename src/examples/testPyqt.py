from PyQt5 import QtWidgets, QtGui, QtCore, uic
import  sys
from src.model.akInstrumentListModel import AkInstrumentListModel





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    #combobox = QtWidgets.QComboBox()
    #combobox.show()

    #listView = QtWidgets.QListView()
    #listView.show()

    #treeView = QtWidgets.QTreeView()
    #treeView.show()

    tableView = QtWidgets.QTableView()
    tableView.show()

    red = QtGui.QColor(255, 0, 0)
    green = QtGui.QColor(0, 255, 0)
    blue = QtGui.QColor(0, 0, 255)

    rowCount = 4
    columnCount = 5

    headers = ["Date", "Open", "High", "Low", "Close"]
    tableData = [ [QtGui.QColor("#FFFF00") for i in range(columnCount)] for j in range(rowCount)]

    model = PalleteTableModel(tableData, headers)
    #model.insertRows(0, 5)
    #model.insertColumns(0, 5)
    #model.removeColumns(0,5)


    #model = AkNameListModel(headers)


    #listView.setModel(model)
    #combobox.setModel(model)
    #treeView.setModel(model)
    tableView.setModel(model)


    sys.exit(app.exec_())
