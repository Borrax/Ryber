import sys
from PySide6 import QtCore, QtWidgets


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel(
            'N.I.K.A.', alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label)


if __name__ == '__main__':
    app = QtWidgets.QApplication()
    main_window = MainWindow()
    main_window.resize(600, 400)
    main_window.show()

    sys.exit(app.exec())
