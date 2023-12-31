import speech_recognition as sr


class MyMicrophone(sr.AudioSource):
    def __init__(self, pyaudio_module,
                 pyaudio_instance,
                 audio_stream,
                 initial_data_chunk,
                 device_index=None,
                 sample_rate=None,
                 chunk_size=1024):

        assert device_index is None or isinstance(device_index, int), \
            "Device index must be None or an integer"
        assert sample_rate is None \
            or (isinstance(sample_rate, int) and sample_rate > 0), \
            "Sample rate must be None or a positive integer"
        assert isinstance(chunk_size, int) and chunk_size > 0, \
            "Chunk size must be a positive integer"

        self.initial_data_chunk = initial_data_chunk
        # set up PyAudio
        self.pyaudio_module = pyaudio_module
        self.audio_stream = audio_stream

        self.device_index = device_index if device_index is not None \
            else 0
        self.format = self.pyaudio_module.paInt16  # 16-bit int sampling
        self.SAMPLE_WIDTH = self.pyaudio_module.get_sample_size(self.format)  # size of each sample
        self.SAMPLE_RATE = sample_rate  # sampling rate in Hertz
        self.CHUNK = chunk_size  # number of frames stored in each buffer

        self.audio = pyaudio_instance
        self.stream = None

    def __enter__(self):
        self.stream = MyMicrophone.MicrophoneStream(
            self.audio_stream,
            self.initial_data_chunk
        )

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    class MicrophoneStream(object):
        read_used = 0

        def __init__(self, pyaudio_stream,
                     initial_data_chunk):
            self.pyaudio_stream = pyaudio_stream
            self.initial_data_chunk = initial_data_chunk

        def read(self, size):
            self.read_used += 1
            if self.read_used == 1:
                return self.initial_data_chunk

            return self.pyaudio_stream.read(size, exception_on_overflow=False)

        def close(self):
            self.read_used = 0
