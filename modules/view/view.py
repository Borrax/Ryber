import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal, Slot, QObject


class AIViewSignaller(QObject):
    response_signal = Signal(str)

    def __init__(self):
        pass

    def update_response_text(self, new_text):
        self.response_signal[str].emit(new_text)


class ListeningThread(QtCore.QThread):
    def __init__(self, listen_fn):
        super().__init__()
        self.listen_fn = listen_fn

    def run(self):
        print('Listening...')
        AIViewSignaller.response_signal[str].emit('Listening...')
        while True:
            self.listen_fn()


class GUI:
    def __init__(self, controller):
        self.app = QtWidgets.QApplication()
        self.controller = controller

    def run(self):
        signaller = AIViewSignaller()
        main_window = MainWindow(signaller)
        main_window.resize(600, 400)
        main_window.show()

        self.listening_thread = ListeningThread(
            self.controller.listen
        )

        self.listening_thread.start()

        sys.exit(self.app.exec())


class MainWindow(QtWidgets.QWidget):
    def __init__(self, signaller):
        super().__init__()

        self.signaller = signaller
        self.signaller[str].connect(self.update_response_text)

        self.label = QtWidgets.QLabel(
            'N.I.K.A.', alignment=QtCore.Qt.AlignCenter)

        self.response_label = QtWidgets.QLabel(
            '', alignment=QtCore.Qt.AlignCenter
        )

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.response_label)

    @Slot(str)
    def update_response_text(self, new_text):
        self.response_label.setText(new_text)
