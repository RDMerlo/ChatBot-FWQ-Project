import torch
import torch.nn as nn
import json

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

def load_neural_model(module_dataset = 'null'):

    dict_result = {'success': True, 'message': ''}

    FILE = ''
    if (module_dataset == 'uunit'):
        with open('../assets/json/uunit_dataset_nomat.json', 'r', encoding='utf-8') as json_data:
            intents = json.load(json_data)
        FILE = "../assets/json/dataset-2023-05-15 12_16_25.971656.pth"

    if (module_dataset == 'laravel'):
        with open('../assets/json/intents.json', 'r', encoding='utf-8') as json_data:
            intents = json.load(json_data)
        FILE = "../assets/json/data.pth"

    if (module_dataset == 'null'):
        dict_result['success'] = False
        dict_result['message'] = 'Не удалось определить модуль'
        return dict_result, None, None, None, None, None,

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

    return dict_result, model, intents, all_words, tags, device