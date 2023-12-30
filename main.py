import pyaudio
from vad import Vad

RECORD_TIME = 0.06
FRAME_RATE = 16000
BYTES = pyaudio.paInt16
CHUNK = int(FRAME_RATE * RECORD_TIME)

audio = pyaudio.PyAudio()
input_stream = audio.open(
    format=BYTES,
    channels=1,
    rate=FRAME_RATE,
    frames_per_buffer=CHUNK,
    input=True
)


vad = Vad(RECORD_TIME, FRAME_RATE, CHUNK)
while True:
    vad.has_voice(input_stream)
