from modules.view.view import GUI
from modules.view.ai_ui_signaller import AIViewSignaller

if __name__ == '__main__':
    ui_ai_signaller = AIViewSignaller()
    gui = GUI(ui_ai_signaller)
    gui.run()
