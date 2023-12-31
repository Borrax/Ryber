import speech_recognition as sr
import pyaudio


class MyMicrophone(sr.AudioSource):
    """
        A custom mycrophone class for the speech_recognition to listen from

        Parameters:
        - pyaudio_module: The pyaudio module the system is using
        - pyaudio_instance: Self explanatory
        - audio_stream (PyAudio.Stream): The source stream containing
        the binary data chunks
        - initial_data_chunk (bytes): The furst CHUNK of bytes
        of an audio stream to be processed
        - device_index (int): The index of the input device in the
        pyaudio list
        - sample_rate (int): The sampling rate per second 
        - chunk_size (int): The size of the chunk of bytes of
        audio data
    """

    def __init__(self,
                 audio_stream,
                 initial_data_chunk=None,
                 device_index=1,
                 sample_rate=16000,
                 chunk_size=1024):

        # the initial chunk of audio data if any to be read first
        self.initial_data_chunk = initial_data_chunk
        self.audio_stream = audio_stream

        # the index of the input device
        self.device_index = device_index
        # 16-bit int sampling
        self.format = pyaudio.paInt16
        # size of each sample
        self.SAMPLE_WIDTH = pyaudio.get_sample_size(self.format)
        # sampling rate in Hertz
        self.SAMPLE_RATE = sample_rate
        # number of frames stored in each buffer
        self.CHUNK = chunk_size
        # a pointer to the microphone stream class
        # which will be initialized at 'with' statement
        self.stream = None

    def __enter__(self):
        self.stream = MyMicrophone.MicrophoneStream(
            self.audio_stream,
            self.initial_data_chunk
        )

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # remove any residual chunks in the audio stream
        while self.audio_stream.get_read_available() > 0:
            self.audio_stream.read(self.CHUNK,
                                   exception_on_overflow=False)

    class MicrophoneStream(object):
        read_used = 0

        def __init__(self, pyaudio_stream,
                     initial_data_chunk):
            self.pyaudio_stream = pyaudio_stream
            self.initial_data_chunk = initial_data_chunk

        def read(self, size):
            self.read_used += 1
            if self.read_used == 1 and self.initial_data_chunk is not None:
                return self.initial_data_chunk

            return self.pyaudio_stream.read(size, exception_on_overflow=False)

        def close(self):
            self.read_used = 0
