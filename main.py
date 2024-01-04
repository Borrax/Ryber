import pyaudio
from modules.vad.vad import Vad
from modules.stt.speech_to_text import SpeechToText
from modules.ir.intent_recognizer import IntentRecognizer
from modules.tts.tts import TextToSpeech
from utils.response import Response

FRAME_RATE = 16000
BYTES = pyaudio.paInt16
CHUNK = 1024

audio = pyaudio.PyAudio()
input_stream = audio.open(
    format=BYTES,
    channels=1,
    rate=FRAME_RATE,
    frames_per_buffer=CHUNK,
    input=True
)


vad = Vad(FRAME_RATE, CHUNK)
stt = SpeechToText(
        sample_rate=FRAME_RATE, chunk=CHUNK
)
ir = IntentRecognizer(Response)
tts = TextToSpeech(Response)

print('Listening...')
while True:
    initial_data = input_stream.read(CHUNK)
    if vad.is_voice_detected(initial_data):
        print('Voice detected')
        resp = stt.listen_and_get_text(input_stream,
                                       initial_data)

        print(resp)
        intent = ir.get_intent(resp['text'])
        print(intent)
        resp_tts = tts.get_speech_audio(resp['text'])
        print(resp_tts)
