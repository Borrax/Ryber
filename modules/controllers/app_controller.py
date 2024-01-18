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

    def __init__(self, signaller=None):
        # a manager for the signals between the controller
        # and the view
        self.signaller = signaller
        # the number of frames per second
        self.FRAME_RATE = 16000
        # the frame width of the audio stream
        self.BYTES = pyaudio.paInt16
        # if the app is still trying to help the user
        self.is_helping = False
        # the size of the audio stream buffer
        self.CHUNK = 1024

        self.audio = pyaudio.PyAudio()
        self.input_stream = self.audio.open(
            format=self.BYTES,
            channels=1,
            rate=self.FRAME_RATE,
            frames_per_buffer=self.CHUNK,
            input=True
        )

        # voice activity detecion
        self.vad = Vad(self.FRAME_RATE, self.CHUNK)
        # speech to text
        self.stt = SpeechToText(
            Response,
            sample_rate=self.FRAME_RATE,
            chunk=self.CHUNK
        )
        # intent recognition
        self.ir = IntentRecognizer(Response)
        # text to speech
        self.tts = TextToSpeech(Response)
        # executes the neccessary tasks given by the user
        self.tasks_controller = TaskHandlersController()

    def listen(self):
        """
            Listens for the user's input and helps if needed
        """
        self.send_signal('Listening...')
        initial_data = self.input_stream.read(
            self.CHUNK)
        if self.vad.is_voice_detected(initial_data):
            self.send_signal('Voice detected')
            self.send_signal('Listening to you...')
            resp_stt = self.stt.listen_and_get_text(
                self.input_stream, initial_data)

            if resp_stt['err'] is not None:
                self.handle_error(resp_stt['err'])
                return

            user_input = resp_stt['payload']
            self.send_signal(user_input)
            user_input = user_input.lower()

            if 'thank you' in user_input:
                self.is_helping = False
                return

            if 'nika' not in user_input \
                    and not self.is_helping:
                return

            self.is_helping = True

            user_input = re.sub(r'(nika)|(nico)', '', user_input)
            user_input = user_input.strip()

            self.send_signal('Analyzing what you said...')
            resp_ir = self.ir.get_intent(user_input)

            if resp_ir['err'] is not None:
                self.handle_error(resp_ir['err'])
                return

            print('Intent: ', resp_ir['payload'])
            to_say = self.tasks_controller.handle(
                resp_ir['payload'], user_input
            )

            if to_say is None or '':
                to_say = 'Hmmm wasn\'t able' \
                         ' to find what you were' \
                         ' looking for'

            self.send_signal(to_say)

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

    def send_signal(self, payload):
        print(payload)

        if self.signaller is not None:
            self.signaller.update_response_text(payload)
