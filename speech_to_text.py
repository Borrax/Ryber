import speech_recognition as sr


class SpeechToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone(device_index=1)

    def listen_and_get_text(self):
        r = self.recognizer
        with self.mic as audio_source:
            print('Listening')
            r.adjust_for_ambient_noise(audio_source)
            audio = r.listen(audio_source)

        resp = {
            'err': None,
            'text': None
        }

        try:
            resp['text'] = r.recognize_whisper(audio, language="en")
        except sr.UnknownValueError:
            resp['err'] = 'Unable to figure out what you are saying'
        except Exception:
            resp['err'] = 'Hmmm, something went wrong in my head'

        return resp


stt = SpeechToText()
while True:
    resp = stt.listen_and_get_text()
    print(resp)
