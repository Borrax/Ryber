import json
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer)
from sklearn.model_selection import train_test_split
from intents import intents

model_name = 'bert-base-uncased'
tokenizer = AutoTokenizer.from_pretrained(model_name)

curr_label_id = 0
labels_ids = {}
ids_labels = {}
data = []
for intent in intents:
    curr_label = intent['label']
    if curr_label not in labels_ids:
        labels_ids[intent['label']] = curr_label_id
        ids_labels[curr_label_id] = curr_label
        curr_label_id += 1

    for content in intent['contents']:
        data_element = {
            'content': content,
            'label_id': labels_ids[curr_label]
        }
        data.append(data_element)


def preprocess_fn(data_element):
    encoding = tokenizer(data_element['content'],
                         padding=True,
                         truncation=True)

    encoding['label'] = data_element['label_id']

    return encoding


# wrtie a json file with the intent types to be used
# later at getting user intents
with open('../../models/ir/intent_types.json', 'w') as json_file:
    json.dump({
        'intents_ids': labels_ids,
        'ids_intents': ids_labels
    }, json_file, indent=2)

tokenized_intents = list(map(preprocess_fn, data))
model = AutoModelForSequenceClassification.from_pretrained(
    model_name,
    num_labels=len(labels_ids.keys())
)

train_data, eval_data = train_test_split(
    tokenized_intents,
    test_size=0.2,
    random_state=42
)

trainer_args = TrainingArguments(
    output_dir='../../models/',
    evaluation_strategy='epoch',
    num_train_epochs=7
)

trainer = Trainer(
    model=model,
    args=trainer_args,
    train_dataset=train_data,
    eval_dataset=eval_data,
    tokenizer=tokenizer
)

trainer.train()
trainer.evaluate()
model.save_pretrained('../../models/ir/')
