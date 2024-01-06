import pyaudio
from modules.vad.vad import Vad
from modules.stt.speech_to_text import SpeechToText
from modules.ir.intent_recognizer import IntentRecognizer
from modules.tts.tts import TextToSpeech
from utils.response import Response
from .greeting_handler import greeting_handler
from .get_info_handler import get_info_handler


class AppController:
    def __init__(self):
        FRAME_RATE = 16000
        BYTES = pyaudio.paInt16
        self.is_helping = False
        self.CHUNK = 1024

        self.audio = pyaudio.PyAudio()
        self.input_stream = self.audio.open(
            format=BYTES,
            channels=1,
            rate=FRAME_RATE,
            frames_per_buffer=self.CHUNK,
            input=True
        )

        self.vad = Vad(FRAME_RATE, self.CHUNK)
        self.stt = SpeechToText(
            sample_rate=FRAME_RATE,
            chunk=self.CHUNK
        )
        self.ir = IntentRecognizer(Response)
        self.tts = TextToSpeech(Response)

    def listen_actively(self):
        print('Listening...')
        while True:
            initial_data = self.input_stream.read(
                self.CHUNK)
            if self.vad.is_voice_detected(initial_data):
                print('Voice detected')
                resp_stt = self.stt.listen_and_get_text(
                    self.input_stream, initial_data)

                print(resp_stt)
                if resp_stt['err'] is not None \
                   and self.is_helping:
                    self.say(resp_stt['err'])
                    continue

                user_input = resp_stt['text']
                input_lower = user_input.lower()

                if 'thank you' in input_lower:
                    self.is_helping = False
                    continue

                if 'nika' not in input_lower \
                        and not self.is_helping:
                    continue

                self.is_helping = True

                resp_ir = self.ir.get_intent(user_input)
                to_say = self.handle_intent(
                    resp_ir['payload'], input_lower.replace('nika', '')
                )

                print(to_say)

                self.say(to_say)

    def handle_intent(self, intent, payload=None):
        if intent == 'greeting_casual':
            return greeting_handler()

        if intent == 'get_info':
            return get_info_handler(payload)

        return 'Sorry, haven\'t been programmed' \
               ' to answer yet'

    def say(self, text):
        resp = self.tts.get_speech_audio(text)
        if resp['err'] is None:
            self.tts.play_audio(resp['payload']['audio'])
            return

        resp_err = self.tts.get_speech_audio(resp['err'])
        if resp_err['err'] is None:
            self.tts.play_audio(resp_err['payload']['audio'])
            return

        print('Something totally went wrong with the tts',
              resp_err['err'])
