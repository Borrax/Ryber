import random

resp_greetings = [
    'Hi', 'Hello there', 'Nice to hear you',
    'Hello again', 'Hello', 'What can I do for you?'
]


def greeting_handler():
    return random.choice(resp_greetings)
