intents = []


def append_intent(contents, label):
    intent = {}
    intent['contents'] = contents
    intent['label'] = label

    intents.append(intent)


greetings_casual = [
    'Hello', 'Hi', 'Hey', 'Greetings', 'Hello there'
]

append_intent(greetings_casual, 'greeting_casual')

date_questions = [
    'What\'s the date',
    'What is the date',
    'What\'s the date today',
    'What is the date today',
    'Today is?',
    'Can you tell me the date',
    'What is the current date',
    'What day is it today',
    'What is today\'s date'
]

append_intent(date_questions, 'get_date')

fact_questions = [
    'What is the definition of',
    'Tell me more about',
    'Can you tell me about something',
    'How many are something',
    'How many are there of something',
    'How much is',
    'How can you',
    'Why',
    'Can you tell me more about',
    'Where is',
    'What is',
    'What are',
    'Where to',
    'Find me',
    'Give me information',
]

append_intent(fact_questions, 'get_info')

questions_to_ryber = [
    'Why are you something',
    'How are you something',
    'How are you?'
    'What are you?',
    'What are you doing?',
    'Whar are you something',
    'Are you',
    'Have you',
    'Did you',
    'Is it that you are'
]

append_intent(questions_to_ryber, 'asking_ryber')
