import pandas as pd
import numpy as np
import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import sklearn
import gensim
import time
import pickle
import tensorflow as tf
from nlpmodel.files.path_utils import get_file_path

KERAS_MODEL = get_file_path("sentiment\shihab_model.h5")
TOKENIZER_MODEL = get_file_path("sentiment\shihab_tokenizer.pkl")

model = keras.models.load_model(KERAS_MODEL)
tokenizer = pickle.load(open(TOKENIZER_MODEL, 'rb'))

TEXT_CLEANING_RE = "@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+"

POSITIVE = "POSITIVE"
NEGATIVE = "NEGATIVE"
NEUTRAL = "NEUTRAL"

SENTIMENT_THRESHOLDS = (0.4, 0.7)
SEQUENCE_LENGTH = 300

stop_words = stopwords.words("english")
stemmer = SnowballStemmer("english")


def preprocess(text, stem=False):
    # Remove link,user and special characters
    text = re.sub(TEXT_CLEANING_RE, ' ', str(text).lower()).strip()
    tokens = []
    for token in text.split():
        if token not in stop_words:
            if stem:
                tokens.append(stemmer.stem(token))
            else:
                tokens.append(token)
    return " ".join(tokens)


def decode_sentiment(score, include_neutral=True):
    if include_neutral:
        label = NEUTRAL
        if score <= SENTIMENT_THRESHOLDS[0]:
            label = NEGATIVE
        elif score >= SENTIMENT_THRESHOLDS[1]:
            label = POSITIVE
        return label
    else:
        return NEGATIVE if score < 0.5 else POSITIVE


def predict(text, include_neutral=True, stem=False):
    start_at = time.time()
    # Preprocess Data
    pp_text = preprocess(text, stem)
    # Tokenize text
    x_test = pad_sequences(tokenizer.texts_to_sequences([pp_text]), maxlen=SEQUENCE_LENGTH)
    # Predict
    score = model.predict([x_test])[0]
    # Decode sentiment
    label = decode_sentiment(score, include_neutral=include_neutral)

    return {"label": label, "score": float(score),
            "elapsed_time": time.time() - start_at}


print(predict("i love THE RAIN!"))
print(predict("you are the love of my life <3"))

print(predict("I hate the rain..."))
print(predict("you are my worst enemy and I wish you nothing but an ill fate"))

print(predict("i don't know what i'm doing"))
print(predict("does anyone know the answer?"))
