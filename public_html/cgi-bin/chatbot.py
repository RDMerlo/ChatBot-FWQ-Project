#! /home/d/dimsultano/chatbotfwqproject_ru/public_html/env_chatbot/bin/python3


'''
/home/d/dimsultano/public_html/env/bin/python3
/usr/bin/python3.8
/home/d/dimsultano/public_html/env/bin/python3.8
/home/d/dimsultano/chatbotfwqproject_ru/public_html/env_chatbot/bin/python3
'''

import sys
import cgi

import random
import json
import torch
import torch.nn as nn
import NLP

class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.act1 = torch.nn.Tanh()
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.act2 = torch.nn.Tanh()
        self.l3 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        x = self.l1(x)
        x = self.act1(x)
        x = self.l2(x)
        x = self.act2(x)
        x = self.l3(x)
        return x

sys.stdout.write("Content-Type: application/json")
sys.stdout.write("\n")
sys.stdout.write("\n")

form = cgi.FieldStorage()

result = {}

quest_text = form.getvalue("quest_text", "не задано")
module_dataset = form.getvalue("module_dataset", "null")

if (module_dataset == 'uunit'):
    with open('../assets/json/uunit_dataset_nomat.json', 'r', encoding='utf-8') as json_data:
        intents = json.load(json_data)
    FILE = "../assets/json/dataset-2023-05-15 12_16_25.971656.pth"

if (module_dataset == 'laravel'):
    with open('../assets/json/intents.json', 'r', encoding='utf-8') as json_data:
        intents = json.load(json_data)
    FILE = "../assets/json/data.pth"

if (module_dataset == 'null'):
    result['success'] = False
    result['message'] = 'Не удалось определить модуль'

    sys.stdout.write(json.dumps(result, indent=1))
    sys.stdout.write("\n")

    sys.stdout.close()

data = torch.load(FILE)

device = torch.device('cpu')

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

dict_params_nlp = {
    'bool_ignore_word': True,
    'bool_check_english': True,
    'bool_remove_english': True,
    'bool_obscene_word': True,
    'bool_true_words': True
}

nlp_result = NLP.tokenize_lemmatize(quest_text, dict_params_nlp)


if not nlp_result['check']:
    result['success'] = nlp_result['check']
    result['message'] = nlp_result['msg']

    sys.stdout.write(json.dumps(result, indent=1))
    sys.stdout.write("\n")
    sys.stdout.close()

X = NLP.bag_of_words(nlp_result['data'], all_words)
X = X.reshape(1, X.shape[0])
X = torch.from_numpy(X).to(device)

output = model(X)
_, predicted = torch.max(output, dim=1)

tag = tags[predicted.item()]

sAnswer = ""
probs = torch.softmax(output, dim=1)
prob = probs[0][predicted.item()]
if prob.item() > 0.50:
    for intent in intents['intents']:
        if tag == intent["tag"]:
            sAnswer = random.choice(intent['responses'])
            if tag == "до свидания":
                break
else:
    sAnswer = "Извините, не понял вопроса, попробуйте переформулировать вопрос."


# str(sys.version_info.major) + "." + str(sys.version_info.minor)
result['success'] = True
result['message'] = sAnswer

sys.stdout.write(json.dumps(result, indent=1))
sys.stdout.write("\n")

sys.stdout.close()