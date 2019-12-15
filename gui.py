import os
import sys
from PySide2.QtWidgets import (QApplication, QStyleFactory, QMainWindow, QAction,
                               QLabel, QWidget, QTabWidget, QFrame, QTextEdit, QPushButton, QLineEdit, QFileDialog)
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

        self.widget = MainScreen(self)

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

    def resizeEvent(self, *args, **kwargs):
        self.widget.resize_widget()


class MainScreen(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move(3, 20)
        self.setFixedSize

        resp = requests.get("https://wasabiwallet.io/api/v3/btc/Offchain/exchange-rates")

        rates = ["1 BTC = {0[rate]} {0[ticker]}".format(el) for el in resp.json()]

        self.label = QLabel("\n".join(rates))
        self.label.setParent(self)
        self.label.move(0, 5)

        prvt_key_shift = 30

        label = QLabel('Завантажте приватний ключ', self)
        label.move(0, prvt_key_shift)
        prvt_key_selector = PrivateKeySelector(self)
        prvt_key_selector.move(0, prvt_key_shift+15)

        self.show_key = QTextEdit(self)
        self.show_key.setFixedSize(200, 210)
        self.show_key.setDisabled(True)
        self.show_key.move(320, prvt_key_shift+4)

    def resize_widget(self):
        self.setFixedWidth(self.parent().width()-17)
        self.setFixedHeight(self.parent().height()-40)


class PrivateKeySelector(QTabWidget):

    class Selector(QWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.read_but = QPushButton('Зчитати', self)
            self.read_but.move(210, 145)
            self.read_but.clicked.connect(lambda x: self.read_data())

        def read_data(self):
            pass

    class TextSelector(Selector):

        def __init__(self, main, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.main = main
            label = QLabel('Вставте ключ', self)
            label.move(6, 0)
            self.editor = QTextEdit(self)
            self.editor.move(5, 15)
            self.editor.setFixedSize(285, 120)

        def read_data(self):
            text = self.editor.toPlainText()
            if text:
                self.main.show_key.setText(text)

    class FileSelector(Selector):

        def __init__(self, main, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.main = main
            self.current_path = ''

            label = QLabel('Виберіть файл ключа', self)
            label.move(6, 0)
            self.entry_for_path = QLineEdit(self)
            self.entry_for_path.setReadOnly(True)
            self.entry_for_path.move(5, 15)
            self.entry_for_path.setFixedSize(260, 17)

            but = QPushButton("...", self)
            but.setFixedSize(20, 25)
            but.move(270, 10)
            but.clicked.connect(lambda x: self.get_data_path())

        def get_data_path(self):
            local_path = str(QFileDialog.getOpenFileName(self, "Select Directory", self.current_path)[0])
            if len(local_path) == 0: return
            self.current_path = local_path
            self.entry_for_path.setText(local_path)

        def read_data(self):
            if self.current_path:
                self.main.show_key.setText(open(self.current_path, encoding='utf8').read())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(300, 200)

        self.addTab(self.TextSelector(self.parent()), 'Текстовий ключ')
        self.addTab(self.FileSelector(self.parent()), 'Файловий ключ')


class Line(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setFixedHeight(3)


if __name__ == "__main__":
    app = QApplication([])
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    window = MainWindow(app.primaryScreen().size())
    sys.exit(app.exec_())
