import json
import torch
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from modules.utils.tryexceptdecorator import TryExceptDecorFactory


class IntentRecognizer:
    tryexceptwrapper = TryExceptDecorFactory.for_methods(
        lambda self, e: self.get_default_error_resp()
    )

    def __init__(self, response_class):
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model = (AutoModelForSequenceClassification
                      .from_pretrained('./models/ir/'))
        self.norm_func = torch.nn.Sigmoid()

        self.threshold = 0.55

        self.response = response_class
        with open('./models/ir/intent_types.json', 'r') as intents_json:
            self.intents_info = json.loads(intents_json.read())

    def get_default_error_resp(self):
        return self.response.create(
            err="Something went wrong while trying to "
                "figure out what you want to do")

    @tryexceptwrapper
    def get_intent(self, text):
        encoded = self.tokenizer(text,
                                 return_tensors='pt',
                                 padding=True,
                                 truncation=True)

        logits = self.model(**encoded).logits
        probs = self.norm_func(logits.squeeze().cpu())
        probs = probs.detach().numpy()

        if probs.max() <= self.threshold:
            print(probs.max())
            return self.response.create('Couldn\'t quite get that')

        intent_id = np.argmax(probs, axis=-1)

        payload = self.intents_info['ids_intents'][str(intent_id)]

        return self.response.create(payload=payload)
