import os
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Slot

from config import ROOT_DIR

alignmentFlag = QtCore.Qt.AlignmentFlag


class MainWindow(QtWidgets.QWidget):
    def __init__(self, signaller):
        super().__init__()

        self.addFont('./assets/NovaSquare-Regular.ttf')

        self.signaller = signaller
        self.signaller.response_signal.connect(self.update_response_text)
        self.signaller.loading_app_signal.connect(self.update_main_loading)

        close_btn = QtWidgets.QPushButton(text='X')
        close_btn.setObjectName('close_btn')
        close_btn.clicked.connect(self.close_app_window)
        close_btn.setFixedSize(50, 25)

        self.main_label = QtWidgets.QLabel('')

        self.response_label = QtWidgets.QLabel('')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(close_btn,
                              alignment=alignmentFlag.AlignRight)
        self.layout.addWidget(self.main_label,
                              alignment=alignmentFlag.AlignCenter)
        self.layout.addWidget(self.response_label,
                              alignment=alignmentFlag.AlignCenter)

        with open(os.path.join(
            ROOT_DIR, 'modules/view/main_window.qss'), 'r'
        ) as style_file:
            qss = style_file.read()

        self.resize(600, 400)
        self.setStyleSheet(qss)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowTitle('N.I.K.A.')

    def addFont(self, path):
        """
            Adds a font to the GUI database to be
            used by all the widgets

            Parameters:
            - path (string): The path to the font file
        """
        id = QtGui.QFontDatabase.addApplicationFont(path)

        if id < 0:
            raise Exception('Couldn\'t load font', path)

    @Slot(str)
    def update_response_text(self, new_text):
        self.response_label.setText(new_text)

    @Slot(bool)
    def update_main_loading(self, is_loading):
        if is_loading:
            self.main_label.setText('Loading...')
        else:
            self.main_label.setText('N.I.K.A.')

    def close_app_window(self):
        """
            Closes the app window
        """
        self.close()
