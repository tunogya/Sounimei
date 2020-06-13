from Sounimei import Sounimei
from GUI_main import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QApplication
import sys


class MyWin(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWin, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # mw = MyWin()
    # mw.show()
    # sys.exit(app.exec())
    spider = Sounimei()
    # spider.run()
    spider.collection()