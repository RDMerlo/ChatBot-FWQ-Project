import random
import json
import torch
import torch.nn as nn

import numpy as np

import nltk
nltk.download('punkt') #для работы токенизации
from nltk.tokenize import word_tokenize
import pymorphy2

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


def tokenize_lemmatize(sentence, bool_ignore_word=True):
    arToken = word_tokenize(sentence, language="russian")

    with open('assets/json/stop_symbols.json', 'r') as f:
        ignore_symbols = json.load(f)
    arToken = [w for w in arToken if w not in ignore_symbols]

    morph = pymorphy2.MorphAnalyzer()
    arToken = [morph.parse(token)[0].normal_form for token in arToken]

    if (True):
        with open('assets/json/stop_words2.json', 'r') as f:
            stop_words = json.load(f)
        arToken = [w for w in arToken if w not in stop_words]

    return arToken

def bag_of_words(pattern_sentence, all_words):
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in pattern_sentence:
            bag[idx] = 1
    return bag

with open('assets/json/intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "assets/json/data.pth"
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

bot_name = "Павел"
print("Введите quit чтобы выйти")

while True:
    # sentence = "do you use credit cards?"
    sentence = input("Вы: ")
    if sentence == "quit":
        break

    sentence = tokenize_lemmatize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    print(predicted)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                print(f"{bot_name}: {random.choice(intent['responses'])}")
                if tag == "до свидания":
                    break
    else:
        print(f"{bot_name}: Извините, не понял вопроса, попробуйте переформулировать вопрос.")