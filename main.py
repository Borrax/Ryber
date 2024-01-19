import sys
from PySide6 import QtCore, QtWidgets
from modules.view.view import MainWindow
from modules.view.ai_ui_signaller import AIViewSignaller
from modules.controllers.assistant_controller import AssistantController


class AssistantThread(QtCore.QThread):
    """
        The thread on which the main assistant
        logic runs
    """

    def __init__(self, signaller):
        super().__init__()
        self.signaller = signaller

    def run(self):
        """
            The method invoked when the thread is
            started
        """
        self.signaller.update_app_loading(True)
        controller = AssistantController(self.signaller)
        self.signaller.update_app_loading(False)

        while True:
            controller.listen()


class App:
    """
        The class that initializes all the
        components of the app
    """

    def __init__(self):
        self.app = QtWidgets.QApplication()
        self.signaller = AIViewSignaller()
        self.assistant_thread = AssistantThread(self.signaller)

        self.main_window = MainWindow(
            self.signaller
        )
        self.main_window.resize(600, 400)

    def run(self):
        """
            Starts the application
        """
        self.main_window.show()
        self.assistant_thread.start()

        sys.exit(self.app.exec())


if __name__ == '__main__':
    app = App()
    app.run()
