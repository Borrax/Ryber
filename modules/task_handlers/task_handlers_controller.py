from .greeting_handler import greeting_handler
from .get_info_handler import get_info_handler


class TaskHandlersController:
    """
        Manages all the task handlers
    """

    def __init__(self):
        pass

    def handle(self, task, payload=None):
        """
            Tries to execute a task

            Parameters:
            - task (String): The name of the task/command
            - payload (any): Additional info the handlers
            to work with. Defaults to None.
        """
        if task == 'greeting_casual':
            return greeting_handler()

        if task == 'get_info':
            return get_info_handler(payload)

        return 'Sorry, I haven\'t been programmed' \
               ' to answer yet'
