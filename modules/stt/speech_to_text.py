import speech_recognition as sr
from modules.stt.my_microphone import MyMicrophone


class SpeechToText:
    def __init__(self, pyaudio_module,
                 pyaudio_instance,
                 sample_rate, chunk=1024):
        self.recognizer = sr.Recognizer()
        self.pyaudio_module = pyaudio_module
        self.pyaudio_instance = pyaudio_instance
        self.SAMPLE_RATE = sample_rate
        self.CHUNK = chunk

    def listen_and_get_text(self, audio_stream,
                            initial_data_chunk):
        """
            Listens through the microphone and after some time
            returns an object containing error message or
            the saying
        """
        resp = {
            'err': None,
            'text': None
        }

        r = self.recognizer
        # mic = sr.Microphone(sample_rate=self.SAMPLE_RATE,
        #                     chunk_size=self.CHUNK)
        mic = MyMicrophone(
            self.pyaudio_module,
            self.pyaudio_instance,
            initial_data_chunk=initial_data_chunk,
            audio_stream=audio_stream,
            sample_rate=self.SAMPLE_RATE,
            chunk_size=self.CHUNK
        )
        with mic as audio_source:
            print('Listening')
            # r.adjust_for_ambient_noise(audio_source)
            try:
                audio = r.listen(audio_source, timeout=3)
            except sr.WaitTimeoutError:
                resp['err'] = 'Timed out'
                return resp

        try:
            resp['text'] = r.recognize_whisper(audio, language="en")
        except sr.UnknownValueError:
            resp['err'] = 'Unable to figure out what you are saying'
        except Exception as e:
            print(e)
            resp['err'] = 'Hmmm, something went wrong in my head'

        return resp
