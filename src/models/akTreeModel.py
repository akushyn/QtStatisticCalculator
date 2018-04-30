from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import QVariant

class AkInstrumentGraphModel(QtCore.QAbstractItemModel):
    """INPUTS: Node, QObject"""

    def __init__(self, root, headers=[], parent=None):
        super(AkInstrumentGraphModel, self).__init__(parent)
        self._rootNode = root

        self._headers = headers

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    def columnCount(self, parent):
        return 1

    def data(self, index, role):

        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.name()

    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if index.isValid():

            if role == QtCore.Qt.EditRole:
                node = index.internalPointer()
                node.setName(value)

                return True
        return False

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return QVariant(self._headers[section])
        return QVariant()

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def parent(self, index):

        node = self.getNode(index)
        parentNode = node.parent()

        if parentNode == self._rootNode:
            return QtCore.QModelIndex()

        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):

        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)

        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node

        return self._rootNode

    def insertRow(self, row, node, parent=QtCore.QModelIndex()):
        return self.insertRows(row, 1, [node], parent)

    def insertRows(self, position, rows, nodes, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)
        self.beginInsertRows(parent, position, position + rows - 1)

        for row in range(rows):
            childCount = parentNode.childCount()
            childNode = nodes[row]#AkNode("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)

        self.endInsertRows()

        return success

    def removeRow(self, row, parentIndex):
        return self.removeRows(row, 1, parentIndex)

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):

        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)

        for row in range(rows):
            success = parentNode.removeChild(position)

        self.endRemoveRows()

        return success


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    rootNode = AkNode("Instruments")
    childNode0 = AkInstrumentNode("EURUSD", rootNode)
    childNode1 = AkInstrumentNode("GBPUSD", rootNode)
    childNode2 = AkInstrumentNode("GOLD", rootNode)

    childNode3 = AkSectionNode("Day", childNode0)
    childNode4 = AkSectionNode("Week", childNode0)
    childNode5 = AkSectionNode("Month", childNode0)

    childNode6 = AkSectionNode("Week", childNode1)
    childNode7 = AkSectionNode("Month", childNode1)

    print(rootNode)

    model = AkInstrumentGraphModel(rootNode)

    treeView = QtWidgets.QTreeView()
    treeView.show()

    treeView.setModel(model)

    sys.exit(app.exec_())