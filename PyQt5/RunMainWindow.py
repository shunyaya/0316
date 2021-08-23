import sys
from typing import FrozenSet 
import ToolboxLayout
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    app= QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = ToolboxLayout.Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())