import sys
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Signal, Slot, QObject
from modules.controllers.app_controller import AppController


class AIViewSignaller(QObject):
    response_signal = Signal(str)
    loading_app_signal = Signal(bool)

    def __init__(self):
        super().__init__()

    def update_response_text(self, new_text):
        self.response_signal[str].emit(new_text)

    def update_app_loading(self, is_loading):
        self.loading_app_signal[bool].emit(is_loading)


class AssistantThread(QtCore.QThread):
    def __init__(self, signaller):
        super().__init__()
        self.signaller = signaller

    def run(self):
        controller = AppController(self.signaller)

        while True:
            controller.listen()


class GUI:
    def __init__(self, signaller):
        self.app = QtWidgets.QApplication()
        self.signaller = signaller

        self.main_window = MainWindow(
            self.signaller
        )
        self.main_window.resize(600, 400)
        self.assistant_thread = AssistantThread(self.signaller)

    def run(self):
        self.main_window.show()
        self.assistant_thread.start()

        sys.exit(self.app.exec())


class MainWindow(QtWidgets.QWidget):
    def __init__(self, signaller):
        super().__init__()

        self.signaller = signaller
        self.signaller.response_signal.connect(self.update_response_text)
        self.signaller.loading_app_signal.connect(self.update_main_loading)

        self.main_label = QtWidgets.QLabel(
            '', alignment=QtCore.Qt.AlignCenter)

        self.response_label = QtWidgets.QLabel(
            '', alignment=QtCore.Qt.AlignCenter
        )

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.main_label)
        self.layout.addWidget(self.response_label)

    @Slot(str)
    def update_response_text(self, new_text):
        self.response_label.setText(new_text)

    @Slot(bool)
    def update_main_loading(self, is_loading):
        if is_loading:
            self.main_label.setText('Loading...')
        else:
            self.main_label.setText('N.I.K.A.')
