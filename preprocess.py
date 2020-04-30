#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import os
import glob
import re

import nltk
# nltk.download('stopwords') 
# nltk.download('words')
# nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.corpus import words as common_words
from nltk import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from symspellpy.symspellpy import SymSpell, Verbosity


def loadCommonDictionary():
    try:
        words = common_words.words()
    except OSError:
        print("Common Word Dictionary Not Found")
    else:
        return words

def loadComplexDictionary():
    try: 
        dictionary_path = os.path.join(os.getcwd(), "symspellpy_frequency_dist.txt") 
        return dictionary_path
    except OSError:
        print("File Not Found")



from datetime import datetime
def utc_to_real(utc_ts):
    return datetime.utcfromtimestamp(int(utc_ts)).strftime('%Y-%m-%d %H:%M:%S')


def join_title_and_body(dataset):
    cols = ['post_title', 'post_body']
    dataset['text'] = dataset[cols].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
    dataset.drop(cols, inplace=True, axis=1)


def remove_URLS(text):
    return re.sub(r'http\S+', ' ', text)


def to_lower_case(text):
    return text.lower()


def remove_numbers(text):
    return ' '.join([i for i in text if not i.isdigit()])


def remove_punc(text):
    return re.sub(r'[^\w\s]',' ', text)


def remove_(text):
    return text.replace('_',' ')


def remove_repeat_words(text):
    toRemove = []
    prev = None
    split_text = text.split()
    for index, word in enumerate(split_text):
        if prev == word:
            toRemove.append(index)
        prev = word
    for index in sorted(toRemove, reverse=True):
        del split_text[index]
    return ' '.join(split_text)


def remove_stopwords(text):
    return ' '.join([word for word in text.split() if word not in stopwords.words('english')])


def complex_correction(word):
    suggestions = symObj.lookup(phrase = word, verbosity = Verbosity.CLOSEST, max_edit_distance = 1)
    return suggestions

def spell_check(text):
    split_text = text.split()
    for index, word in enumerate(split_text):
        if word not in commonWords:
            suggestions = complex_correction(word)
            if len(suggestions) != 0:
                split_text[index] = split_text[index].replace(word, suggestions[0].term)
    return ' '.join(split_text)

def tokenize(text):
    tokens = word_tokenize(text)
    return tokens

def lemmatize(tokens):
    lmtzr = WordNetLemmatizer()
    lemmatized_tokens = [lmtzr.lemmatize(t) for t in tokens]
    return lemmatized_tokens

symObj = SymSpell(max_dictionary_edit_distance = 2, prefix_length = 7, compact_level = 2)
commonWords = loadCommonDictionary()
dictionary = loadComplexDictionary()
symObj.load_dictionary(dictionary, term_index = 0, count_index = 1)

#### UNCOMMENT THIS IF YOU WANT TO RUN DIRECTLY IN SCRIPT ---> ####

# os.getcwd() #'C:\\Users\\ThomasTheisen\\Documents\\suicidewatchdata'
# # os.chdir('/Users/michellemorales/Box Sync/IBM_CLPsych19/data_sample_clpsych19/') # use this to change dir if your data is stored somewhere else
# mylist = [f for f in glob.glob("*.csv")]

# cleaned_data = []
# columns = ['post_id', 'user_id', 'timestamp', 'subreddit', 'post_title', 'post_body']
# _data = pd.DataFrame(columns=columns)
# for file in mylist:
#     d = pd.read_csv(file)
#     data = _data.append(d, ignore_index=True)
#     data['timestamp'] = data.apply(lambda x: utc_to_real(x['timestamp']), axis=1)
#     join_title_and_body(data)
#     data['text'] = data.apply(lambda x: remove_URLS(x['text']), axis=1)
#     data['text'] = data.apply(lambda x: to_lower_case(x['text']), axis=1)
#     data['text'] = data.apply(lambda x: remove_numbers(x['text']), axis=1)
#     data['text'] = data.apply(lambda x: remove_punc(x['text']), axis=1)
#     data['text'] = data.apply(lambda x: remove_(x['text']), axis=1)
#     data['text'] = data.apply(lambda x: remove_repeat_words(x['text']), axis=1)
#     data['text'] = data.apply(lambda x: spell_check(x['text']), axis=1)
#     data['text'] = data.apply(lambda x: remove_stopwords(x['text']), axis=1)
#     data['tokens'] = data.apply(lambda x: tokenize(x['text']), axis=1) # Tokenize text
#     data['tokens'] = data.apply(lambda x: lemmatize(x['tokens']), axis=1) # Lemmatize tokens
#     cleaned_data.append(data)