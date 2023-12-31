import numpy as np
import torch
import copy


class Vad:
    """
        A class encapsulating the voice activity
        detection logic

        Parameters:
        - frame_rate (int): the number of frames per second,
        either 8000 or 16000,
        - chunk (int): the number of frames per buffer

        Attributes:
        - VOICE_THRESHOLD (float): A value between 0 and 0.99
        above which the confidence of the model is enough to
        say that it has detected voice
    """

    ONE_DIV_HALF_INT16 = 1 / 32768
    VOICE_THRESHOLD = 0.85

    def __init__(self,
                 frame_rate,
                 chunk):
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

    def is_voice_detected(self, data):
        """
            Checks if the audio stream has notable voice

            Parameters:
            - stream (PyAudio.Stream): the raw audio stream
            from pyaudio
        """
        audio_int16 = np.frombuffer(data, dtype=np.int16)
        audio_f32 = self.int16_to_float32(audio_int16)

        probability = self.model(torch.from_numpy(audio_f32),
                                 self.FRAME_RATE).item()

        if probability > self.VOICE_THRESHOLD:
            print(probability)
            return True

        return False
