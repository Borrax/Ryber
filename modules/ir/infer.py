import torch
import numpy as np
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from train import trainer, ids_labels

model_path = '../../models/ir/'

model = AutoModelForSequenceClassification.from_pretrained(
    model_path
)

tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')


def get_ir_label(text):
    encoding = tokenizer(text,
                         return_tensors='pt',
                         padding=True,
                         truncation=True)

    encoding = {k: v.to(trainer.model.device) for k, v in encoding.items()}

    outputs = model(**encoding)
    logits = outputs.logits

    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(logits.squeeze().cpu())
    probs = probs.detach().numpy()
    print(probs)
    label_id = np.argmax(probs, axis=-1)

    return ids_labels[label_id]


print(get_ir_label('Why are there stars in the sky'))
