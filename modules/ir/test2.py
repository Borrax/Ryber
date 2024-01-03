import json
import torch
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class IntentReognizer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
        self.model = (AutoModelForSequenceClassification
                      .from_pretrained('../../models/ir/'))
        self.norm_func = torch.nn.Sigmoid()

        with open('../../models/ir/intent_types.json', 'r') as intents_json:
            self.intents_info = json.loads(intents_json.read())

        self.threshold = 0.55

    def build_resp(self, err=None, payload=None):
        return {
            'err': err,
            'payload': payload
        }

    def get_intent(self, text):
        encoded = self.tokenizer(text,
                                 return_tensors='pt',
                                 padding=True,
                                 truncation=True)

        logits = self.model(**encoded).logits
        probs = self.norm_func(logits.squeeze().cpu())
        probs = probs.detach().numpy()

        if probs.max() <= self.threshold:
            return self.build_resp('Couldn\'t quite get that')

        intent_id = np.argmax(probs, axis=-1)

        payload = self.intents_info['ids_intents'][str(intent_id)]

        return self.build_resp(payload=payload)


IR = IntentReognizer()
print(IR.get_intent('What are the stars'))
