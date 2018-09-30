from PyQt5 import QtWidgets, QtCore, QtGui

class ListDelegate(QtWidgets.QStyledItemDelegate):

  def createEditor(self, parent, option, index):
    editor = QtWidgets.QComboBox(parent)
    for i in range( 12 ):
      editor.addItem('list item %d' % i)

    return editor

if __name__ == '__main__':

  import sys

  app = QtWidgets.QApplication(sys.argv)

  model = QtGui.QStandardItemModel(2, 2)
  tableView = QtWidgets.QTableView()

  delegate = ListDelegate()
  tableView.setItemDelegate(delegate)

  tableView.setModel(model)

  for row in range(2):
    for column in range(2):

      item = QtGui.QStandardItem( 'None' )

      model.setItem(row, column, item)

  tableView.setWindowTitle('example')
  tableView.show()
  sys.exit(app.exec_())