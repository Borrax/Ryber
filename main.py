from modules.controllers.app_controller import AppController
from modules.view.view import GUI, AIViewSignaller

if __name__ == '__main__':
    ui_ai_signaller = AIViewSignaller()
    controller = AppController(ui_ai_signaller)
    gui = GUI(controller, ui_ai_signaller)
    gui.run()
