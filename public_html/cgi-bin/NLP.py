import math
import numpy as np
import json
import re

import nltk
nltk.download('punkt')  # для работы токенизации
from nltk.tokenize import word_tokenize
import pymorphy2


def remove_english_words(vector, remove_empty_item=True):
    '''Удаление английских символов'''
    pattern = re.compile('[a-zA-Z]')
    for i in range(len(vector)):
        vector[i] = re.sub(pattern, '', vector[i])
    if (remove_empty_item):
        vector = ' '.join(vector).split()
    return vector


def tokenize_lemmatize(sentence, tmp_dict_params_nlp):
    dict_result = {'check': True, 'data': None, 'msg': ''}

    dict_params_nlp = {
        'bool_ignore_word': True,
        'bool_check_english': True,
        'bool_remove_english': True,
        'bool_obscene_word': True,
        'bool_true_words': True
    }

    for key in tmp_dict_params_nlp:
        dict_params_nlp[key] = tmp_dict_params_nlp[key]

    text_sentence = sentence

    sentence = re.sub(r'[^\w\s]', '', sentence)
    arTokens = word_tokenize(sentence, language="russian")

    if (dict_params_nlp['bool_check_english'] and len(arTokens) != 0):
        english_words = re.findall(r'[a-zA-Z]+', text_sentence)

        if (len(arTokens) != 0):
            procent_english_words = len(english_words) / (len(arTokens) / 100)
        else:
            procent_english_words = 0

        if (procent_english_words > 50.0):
            dict_result['check'] = False
            dict_result['msg'] = 'Текст в основном на английском.'
            dict_result['data'] = arTokens
            return dict_result

        if (dict_params_nlp['bool_remove_english']):
            arTokens = remove_english_words(arTokens)

    morph = pymorphy2.MorphAnalyzer()
    arLems = [morph.parse(token)[0].normal_form for token in arTokens]

    if (dict_params_nlp['bool_ignore_word']):
        with open('../assets/json/stop_words2.json', 'r') as f:
            stop_words = json.load(f)
        arLems = [w for w in arLems if w not in stop_words]

    # нецензурная лексика
    if (dict_params_nlp['bool_obscene_word']):
        with open('../assets/json/mats.json', 'r') as f:
            obscene_words = json.load(f)
        for w in arLems:
            if w in obscene_words:
                dict_result['check'] = False
                dict_result['msg'] = 'Пожалуйста, ведите себя вежливо!'
                dict_result['data'] = arLems
                return dict_result

    # проверка на бессмылицу
    if (dict_params_nlp['bool_true_words'] and len(arLems) != 0):
        with open('../assets/json/DictionaryRussianWords.txt', 'r') as f:
            rus_dict_word = f.readlines()

        count_all_words = len(arLems)
        count_find_words = 0
        for word in arLems:
            if (word + '\n') in rus_dict_word:
                count_find_words += 1

        procent_true_words = count_find_words / (count_all_words / 100)

        if (procent_true_words < 50.0):
            dict_result['check'] = False
            dict_result['msg'] = 'Не удалось распознать слова'
            dict_result['data'] = arLems
            return dict_result

    dict_result['check'] = True
    dict_result['msg'] = 'Обработка прошла успешно.'
    dict_result['data'] = arLems
    return dict_result


def words_processing(intents, tmp_dict_params_nlp):
    all_words = []
    tags = []
    xy = []
    # проходимся по сущностям
    for intent in intents['intents']:
        tag = intent['tag']  # сохраняем тэг
        tags.append(tag)
        # проходимся по паттернам
        for pattern in intent['patterns']:
            result = tokenize_lemmatize(pattern, tmp_dict_params_nlp)
            if (result['check']):
                all_words.extend(result['data'])
                xy.append((result['data'], tag))
    # удаляем дупликаты и сортируем
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))
    return all_words, tags, xy


def bag_of_words(pattern_sentence, all_words):
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in pattern_sentence:
            bag[idx] = 1
    return bag


def tf(all_words, pattern_sentence):
    tf = np.zeros(len(all_words), dtype=np.float32)
    # проходимся по каждому слову из словаря и смотрим, есть ли он в документе
    for idx, w in enumerate(all_words):
        if w in pattern_sentence:
            tf[idx] += 1 / len(pattern_sentence)

    return tf


def idf(all_words, xy):
    # количество документов в котором встречается слово
    count_pattern = np.zeros(len(all_words), dtype=np.float32)

    for idx, w in enumerate(all_words):
        # #проходимся по каждому документу
        for (pattern_sentence, tag) in xy:
            if w in pattern_sentence:
                count_pattern[idx] += 1

    idf = [math.log(len(xy) / count_pattern) for count_pattern in count_pattern]
    return idf