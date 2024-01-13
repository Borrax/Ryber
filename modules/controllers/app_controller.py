import re
import pyaudio
from modules.vad.vad import Vad
from modules.stt.speech_to_text import SpeechToText
from modules.ir.intent_recognizer import IntentRecognizer
from modules.tts.tts import TextToSpeech
from modules.utils.response import Response
from modules.task_handlers.task_handlers_controller \
    import TaskHandlersController


class AppController:
    """
        Orchastrates the different modules of the program
        amd provides interface to the back-end logic
    """

    def __init__(self):
        # the number of frames per second
        FRAME_RATE = 16000
        # the frame width of the audio stream
        BYTES = pyaudio.paInt16
        # if the app is still trying to help the user
        self.is_helping = False
        # the size of the audio stream buffer
        self.CHUNK = 1024

        self.audio = pyaudio.PyAudio()
        self.input_stream = self.audio.open(
            format=BYTES,
            channels=1,
            rate=FRAME_RATE,
            frames_per_buffer=self.CHUNK,
            input=True
        )

        print('Loading...')
        # voice activity detecion
        self.vad = Vad(FRAME_RATE, self.CHUNK)
        # speech to text
        self.stt = SpeechToText(
            Response,
            sample_rate=FRAME_RATE,
            chunk=self.CHUNK
        )

        # intent recognition
        self.ir = IntentRecognizer(Response)
        # text to speech
        self.tts = TextToSpeech(Response)
        # executes the neccessary tasks given by the user
        self.tasks_controller = TaskHandlersController()

    def listen_actively(self):
        """
            Listens indefinetely to the user and
            executes tasks if needed
        """
        print('Listening...')
        while True:
            initial_data = self.input_stream.read(
                self.CHUNK)
            if self.vad.is_voice_detected(initial_data):
                print('Voice detected')
                print('Listening to you...')
                resp_stt = self.stt.listen_and_get_text(
                    self.input_stream, initial_data)

                if resp_stt['err'] is not None:
                    self.handle_error(resp_stt['err'])
                    continue

                user_input = resp_stt['payload']
                print('You said:', user_input)
                user_input = user_input.lower()

                if 'thank you' in user_input:
                    self.is_helping = False
                    continue

                if 'nika' not in user_input \
                        and not self.is_helping:
                    continue

                self.is_helping = True

                user_input = re.sub(r'(nika)|(nico)', '', user_input)
                user_input = user_input.strip()

                print('Analyzing what you said...')
                resp_ir = self.ir.get_intent(user_input)

                if resp_ir['err'] is not None:
                    self.handle_error(resp_ir['err'])
                    continue

                print('Intent: ', resp_ir['payload'])
                to_say = self.tasks_controller.handle(
                    resp_ir['payload'], user_input
                )

                if to_say is None:
                    to_say = 'Hmmm wasn\'t able' \
                             ' to find what you were' \
                             ' looking for'

                print('My response:', to_say)

                self.say(to_say)

    def say(self, text):
        """
            Says the text to the user

            Paramters:
            - text (string): The text that needs to be
            said verbally
        """
        resp = self.tts.get_speech_audio(text)
        if resp['err'] is None:
            self.tts.play_audio(resp['payload']['audio'])
            return

        self.handle_error(resp['err'])

    def handle_error(self, err_msg):
        """
            Does the necessary operations when an error message
            has occured.

            Parameters:
            - err_msg (string): The message of the error to e shown
        """
        if self.is_helping:
            resp = self.tts.get_speech_audio(err_msg)
            if resp['payload'] is not None:
                self.tts.play_audio(resp['payload']['audio'])
            else:
                print('Something went wrong with the tts')

        print(err_msg)
