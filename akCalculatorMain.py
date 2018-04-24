import sys
from PyQt5 import QtWidgets
from src.controllers.akCalculatorController import AkCalculatorController

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = AkCalculatorController()
    application.show()
    sys.exit(app.exec_())