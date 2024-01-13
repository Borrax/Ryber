import sys
from PySide6 import QtCore, QtWidgets


class ListeningThread(QtCore.QThread):
    def __init__(self, listen_fn):
        super().__init__()
        self.listen_fn = listen_fn

    def run(self):
        print('Listening...')
        while True:
            self.listen_fn()


class GUI:
    def __init__(self, controller):
        self.app = QtWidgets.QApplication()
        self.controller = controller

    def run(self):
        main_window = MainWindow()
        main_window.resize(600, 400)
        main_window.show()

        self.listening_thread = ListeningThread(
            self.controller.listen
        )

        self.listening_thread.start()

        sys.exit(self.app.exec())


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel(
            'N.I.K.A.', alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label)
