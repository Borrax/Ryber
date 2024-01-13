from modules.controllers.app_controller import AppController
from modules.view.view import GUI

if __name__ == '__main__':
    controller = AppController()
    gui = GUI(controller)
    gui.run()
