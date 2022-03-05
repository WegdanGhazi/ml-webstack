# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 18:15:29 2021

@author: Wegdan
"""
import numpy as np
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout
from keras.preprocessing.text import Tokenizer
from keras.callbacks import EarlyStopping
from keras.models import Sequential
import keras.utils as ku 
from keras.models import model_from_json
from pynput import keyboard
from nlpmodel.files.path_utils import get_file_path

#function to encode character inputs
def tokenize(input_string):
    tokenizer = Tokenizer(num_words=None,
                          char_level=True,
                          oov_token=None)
    corpus = input_string.lower()  
    tokenizer.fit_on_texts(corpus)
    return tokenizer

def encode(tokenizer, text):
    output = tokenizer.texts_to_sequences([text])[0]
    output = np.array(output)/float(len(tokenizer.index_word.keys()))
    return output

def encode_y(tokenizer, text):
    output = tokenizer.texts_to_sequences([text])[0]
    return output

def load_model():
    json_file = open(get_file_path("prediction\model.json"), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(get_file_path("prediction\model.h5"))
    print("Loaded model from disk")
    return loaded_model

def predict_next_character(X_test, tokenizer, model, max_length):
    input_length = len(X_test)
    if(input_length > max_length):
        X_test = X_test[input_length - max_length + 1 :-1]
    encoded_input = encode(tokenizer, X_test)
    encoded_input = pad_sequences([encoded_input], maxlen=max_length, padding='pre', dtype='float32')
    encoded_input = np.reshape(encoded_input, (1, max_length, 1))
    prediction = model.predict(encoded_input, verbose=0)
    index = np.argmax(prediction)
    next_char = tokenizer.sequences_to_texts([[index]])
    return next_char

### incremental prediction

def predict(input_string, tk, model, max_sequence_len):
    new_word = input_string.split()[-1] if input_string[-1] != " " and input_string else ""
    next_char = ""
    while next_char != " ":
        next_char = predict_next_character(input_string, tk, model, max_sequence_len)[0]
        input_string += next_char
        new_word += next_char
    return new_word

def predict_sentence(input_string):
    max_sequence_len = 100
    return predict(input_string, tk, model, max_sequence_len)


input_data = open(get_file_path("prediction\84-0.txt"), encoding="utf8").read()
input_data = input_data.replace('\n', '')
input_data = input_data.replace('\ufeff', '')
# this is the dictionary/tokenizer which will be used 
tk = tokenize(input_data)
model = load_model()
