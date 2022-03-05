
import pickle

import numpy as np
import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.stem import RegexpStemmer
from nlpmodel.files.path_utils import get_file_path

nltk.download('wordnet')
nltk.download('stopwords')

word_stemmer = PorterStemmer()
Reg_stemmer = RegexpStemmer(r'ing$|ed$')
def create_df(sentence):
    df = pd.DataFrame([sentence],columns=['news'])

    return df
df = create_df('World Economy drops')

def Reg(x):
    return [Reg_stemmer.stem(i) for i in x.split()]


def lem(x):
    return [lemmatizer.lemmatize(i) for i in x.split()]

PREDICTION_DICT = {
1:'World',
2:'Sports',
3:'Business',
4:'Sci/Tech'
}

# Init the Wordnet Lemmatizer
lemmatizer = WordNetLemmatizer()
df['News_lemm'] = df['news'].apply(lambda x: ' '.join(lem(x)))
df['Header_lemm'] = df['news'].apply(lambda x: ' '.join(lem(x)))
df['News_reg'] = df['News_lemm'].apply(lambda x: ' '.join(Reg(x)))
df['Header_reg'] = df['Header_lemm'].apply(lambda x: ' '.join(Reg(x)))
print(df)
def predict(df):
    pkl_sgd = get_file_path('detection\SGD_Header.pkl')
    pkl_xgb = get_file_path('detection\XGB_News.pkl')
    with open(pkl_sgd, 'rb') as file:
        model_sgd = pickle.load(file)

    with open(pkl_xgb, 'rb') as file:
        model_xgb = pickle.load(file)
    print(model_xgb.predict(df['News_reg']))
    print(model_sgd.predict(df['Header_reg']))
    preds = model_xgb.predict(df['News_reg'])
    return PREDICTION_DICT[preds[0]]

predict(df)

def predict_topic(sentence):
    df = create_df(sentence)
    df['News_lemm'] = df['news'].apply(lambda x: ' '.join(lem(x)))
    df['Header_lemm'] = df['news'].apply(lambda x: ' '.join(lem(x)))
    df['News_reg'] = df['News_lemm'].apply(lambda x: ' '.join(Reg(x)))
    df['Header_reg'] = df['Header_lemm'].apply(lambda x: ' '.join(Reg(x)))
    return predict(df)