import sys
from pyxing.session import *
from PyQt5.QtWidgets import *


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.xasession = XASession()
        self.xasession.login("id", "password", "cert", block=False)

        # button
        self.button = QPushButton("계좌 조회", self)
        self.button.move(10, 10)
        self.button.clicked.connect(self.get_account)

    def get_account(self):
        account = self.xasession.get_account_list(0)
        self.statusBar().showMessage(account)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()