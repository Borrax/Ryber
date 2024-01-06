import speech_recognition as sr
from modules.stt.my_microphone import MyMicrophone


class SpeechToText:
    """
        Provides a speech to text model interface

        Parameters:
        - response_class: A static class or instance that
        has methods that create response objects that this
        interface interface would return
        - sample_rate: The sampling rate of the audio stream
        it will analyze
        - chunk: The number of bits it will process at a time
    """

    def __init__(self, response_class,
                 sample_rate=16000, chunk=1024):
        self.response = response_class
        self.SAMPLE_RATE = sample_rate
        self.CHUNK = chunk
        self.recognizer = sr.Recognizer()

    def listen_and_get_text(self, audio_stream,
                            initial_data_chunk):
        """
            Listens through the microphone and after some time
            returns an object containing error message or
            the saying
        """
        resp = self.response.create()

        r = self.recognizer

        mic = MyMicrophone(
            initial_data_chunk=initial_data_chunk,
            audio_stream=audio_stream,
            sample_rate=self.SAMPLE_RATE,
            chunk_size=self.CHUNK
        )
        with mic as audio_source:
            try:
                audio = r.listen(audio_source, timeout=3)
            except sr.WaitTimeoutError:
                resp['err'] = 'Timed out trying to figure what you were saying'
                return resp

        try:
            resp['payload'] = r.recognize_whisper(audio, language="en").strip()
        except sr.UnknownValueError:
            resp['err'] = 'Unable to figure out what you are saying'
        except Exception as e:
            print(e)
            resp['err'] = 'Hmmm, something went wrong in my head'

        return resp
