import sys
from PySide6 import QtCore, QtWidgets
from modules.view.view import MainWindow
from modules.view.ai_ui_signaller import AIViewSignaller
from modules.controllers.assistant_controller import AssistantController


class AssistantThread(QtCore.QThread):
    def __init__(self, signaller):
        super().__init__()
        self.signaller = signaller

    def run(self):
        self.signaller.update_app_loading(True)
        controller = AssistantController(self.signaller)

        self.signaller.update_app_loading(False)
        while True:
            controller.listen()


class App:
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


if __name__ == '__main__':
    ui_ai_signaller = AIViewSignaller()
    app = App(ui_ai_signaller)
    app.run()
