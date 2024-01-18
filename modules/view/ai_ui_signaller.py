from PySide6.QtCore import QObject, Signal


class AIViewSignaller(QObject):
    response_signal = Signal(str)
    loading_app_signal = Signal(bool)

    def __init__(self):
        super().__init__()

    def update_response_text(self, new_text):
        self.response_signal[str].emit(new_text)

    def update_app_loading(self, is_loading):
        self.loading_app_signal[bool].emit(is_loading)
