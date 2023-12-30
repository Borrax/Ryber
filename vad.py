import pyaudio
import numpy as np
import torch


class Vad:
    """
        A class encapsulating the voice activity
        detection logic

        Parameters:
        - record_time (float|int): The chunk of microphone time
        (in seconds) recording that will be analyzed
        - frame_rate (int): the number of frames per second,
        either 8000 or 16000,
        - chunk (int): the number of frames per buffer
    """

    ONE_DIV_HALF_INT16 = 1 / 32768

    def __init__(self, record_time,
                 frame_rate,
                 chunk):
        self.RECORD_TIME = record_time
        self.FRAME_RATE = frame_rate
        self.CHUNK = chunk

        torch.set_num_threads(1)
        self.model = torch.jit.load('./models/vad/silero_vad.jit',
                                    map_location=torch.device('cpu'))
        self.model.eval()

    def int16_to_float32(self, audio_arr):
        abs_max = np.abs(audio_arr).max()
        audio_arr = audio_arr.astype('float32')

        if abs_max > 0:
            audio_arr *= self.ONE_DIV_HALF_INT16

        return audio_arr

    def has_voice(self, stream):
        """
            Checks if the audio stream has notable voice

            Parameters:
            - stream (PyAudio.Stream): the raw audio stream
            from pyaudio
        """
        data = stream.read(self.CHUNK)
        audio_int16 = np.frombuffer(data, dtype=np.int16)
        audio_f32 = self.int16_to_float32(audio_int16)

        probability = self.model(torch.from_numpy(audio_f32),
                                 self.FRAME_RATE).item()

        if probability > 0.85:
            print(probability)
            return True

        return False


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
