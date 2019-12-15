import os
import sys
from PySide2.QtWidgets import QApplication, QStyleFactory, QMainWindow, QAction, QLabel
import requests


class MainWindow(QMainWindow):
    def __init__(self, screen_param):
        super(MainWindow, self).__init__()
        self.setWindowTitle("GingerWallet")
        self.screen_param = screen_param
        desired_size = (802, 530)

        self.setMinimumSize(desired_size[0]//2, desired_size[1])
        self.set_size(desired_size)
        self.root_path = os.getcwd()

        self.program = 0

        firstAction = QAction("Wallet", self)
        #firstAction.triggered.connect(self.show_stats)
        secondAction = QAction("Options", self)
        #secondAction.triggered.connect(self.show_options)

        self.statusBar()
        mainMenu = self.menuBar()
        opt1 = mainMenu.addMenu('&Program')
        opt1.addAction(firstAction)
        opt1.addAction(secondAction)

        resp = requests.get("https://wasabiwallet.io/api/v3/btc/Offchain/exchange-rates")

        rates = ["{0[ticker]} : {0[rate]}".format(el) for el in resp.json()]

        self.label = QLabel("\n".join(rates))
        self.label.setParent(self)
        self.label.move(50, 0)


        #resp = requests.get("https://wasabiwallet.io/api/v3/btc/Blockchain/transaction-hexes?"
        #                    "transactionIds=c553ad2c6ae9c8200f2185e8ef23740abda5b19be592eb0c5b4e7810045ff41d&"
        #                    "transactionIds=687b25fb255cf4d401fea6087ce82a561d07d538b16b54ccb7489b23d32e825b")

        #print(resp.json())

        self.show()

    def restore_root(self):
        os.chdir(self.root_path)

    def set_size(self, desired_size):
        self.setGeometry(
            (self.screen_param.width() - desired_size[0]) / 2,
            (self.screen_param.height() - desired_size[1]) / 2,
            desired_size[0],
            desired_size[1]
        )


if __name__ == "__main__":
    app = QApplication([])
    QApplication.setStyle(QStyleFactory.create("Windows"))
    window = MainWindow(app.primaryScreen().size())
    sys.exit(app.exec_())
