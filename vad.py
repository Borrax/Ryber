import pyaudio
import numpy as np
import torch

torch.set_num_threads(1)

model = torch.jit.load('./models/vad/silero_vad.jit',
                       map_location=torch.device('cpu'))
model.eval()

# in seconds
RECORD_TIME = 0.1
FRAME_RATE = 16000
CHUNK = int(RECORD_TIME * FRAME_RATE)

audio = pyaudio.PyAudio()
input_stream = audio.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=FRAME_RATE,
    input=True,
    frames_per_buffer=CHUNK,
)


def int16_to_float32(audio_arr):
    abs_max = np.abs(audio_arr).max()
    audio_arr = audio_arr.astype('float32')

    if abs_max > 0:
        audio_arr *= 1/32768

    return audio_arr


while True:
    data = input_stream.read(CHUNK)
    audio_arr = np.frombuffer(data, dtype=np.int16)
    audio_arr_f32 = int16_to_float32(audio_arr)

    conf = model(torch.from_numpy(audio_arr_f32),
                 FRAME_RATE)

    print(conf)
