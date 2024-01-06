import os
import torch
import soundfile as sf
from transformers import (SpeechT5ForTextToSpeech,
                          SpeechT5Processor, SpeechT5HifiGan)
from datasets import load_dataset
from pydub import AudioSegment
from pydub.playback import play
from utils.tryexceptdecorator import TryExceptDecorFactory
from config import ROOT_DIR


class TextToSpeech:
    tryexceptwrapper = TryExceptDecorFactory.for_methods(
        lambda self, e: self.response_class.create(
            err='Something went wrong while trying to'
                ' tell you my thought'
        )
    )

    def __init__(self, response_class):
        self.response_class = response_class
        self.output_filepath = os.path.join(ROOT_DIR, 'modules/tts/speech.wav')
        self.device = ('cuda' if torch.cuda.is_available()
                       else 'cpu')

        model_name = 'microsoft/speecht5_tts'
        gan_name = 'microsoft/speecht5_hifigan'
        dataset_name = 'Matthijs/cmu-arctic-xvectors'
        speaker_id = 2411

        self.tokenizer = SpeechT5Processor.from_pretrained(model_name)

        self.model = SpeechT5ForTextToSpeech.from_pretrained(
            model_name
        ).to(self.device)

        # encodes the voice to digital sounds
        self.vocoder = SpeechT5HifiGan.from_pretrained(
            gan_name).to(self.device)

        data = load_dataset(dataset_name, split='validation')

        self.speaker_embeddings = torch.tensor(
            data[speaker_id]['xvector']
        ).unsqueeze(0).to(self.device)

    @tryexceptwrapper
    def get_speech_audio(self, text):
        encoding = self.tokenizer(
            text=text, return_tensors='pt').to(self.device)

        speech = self.model.generate_speech(
            encoding['input_ids'],
            self.speaker_embeddings,
            vocoder=self.vocoder
        )

        sf.write(
            self.output_filepath,
            speech.cpu().numpy(),
            samplerate=16000
        )

        audio = AudioSegment.from_file(
            self.output_filepath,
            format='wav'
        )

        payload = {
            'audio': audio,
        }

        return self.response_class.create(
            payload=payload
        )

    def play_audio(self, audio):
        play(audio)
