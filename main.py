from src import BRLPlayer
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from src.MainWindow import BRLMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    p = BRLMainWindow()
    p.show()
    sys.exit(app.exec_())
