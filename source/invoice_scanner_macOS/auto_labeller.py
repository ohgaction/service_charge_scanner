#!/usr/bin/env python3

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

import cv2
import re
import os
import json
import shutil
import pathlib
import pytesseract
from pytesseract import Output
from datetime import datetime
from getkey import getkey
from tkinter import *
from tkinter import filedialog
from PIL import Image
from pdf2image import convert_from_path


def build_auto_classifier():

    filepath_dict = {'training_data/learning_data': 'training_data/learning_data.csv'}
    df_list = []
    for source, filepath in filepath_dict.items():
        df = pd.read_csv(filepath, names=['sentence', 'label'], sep='\t')
        df['source'] = source  # Add another column filled with the source name
        df_list.append(df)

    df = df.reset_index()
    df = pd.concat(df_list)
    #print(df)

    for source in df['source'].unique():
        df_source = df[df['source'] == source]
        sentences = df_source['sentence'].values
        y = df_source['label'].values

        sentences_train, sentences_test, y_train, y_test = train_test_split(
            sentences, y, test_size=0.300, random_state=1000)

        vectorizer = CountVectorizer()
        vectorizer.fit(sentences_train)
        X_train = vectorizer.transform(sentences_train)
        X_test  = vectorizer.transform(sentences_test)

        classifier = LogisticRegression()
        classifier.fit(X_train, y_train)
        score = classifier.score(X_test, y_test)
        print('Accuracy for {} data: {:.4f}'.format(source, score))

    return vectorizer, classifier


def auto_classifier(vectorizer, classifier, input):

    threshold = 0.5
    classification = ""
    new_test_data = []

    new_test_data.append(input)
    new_x_test  = vectorizer.transform(new_test_data)
    percentages = classifier.predict_proba(new_x_test)
#    results = classifier.predict(new_x_test)

    if percentages[0,0] > threshold:
        classification = 1

    if percentages[0,1] > threshold:
        classification = 2

    if percentages[0,2] > threshold:
        classification = 3

    if percentages[0,3] > threshold:
        classification = 4

    if percentages[0,4] > threshold:
        classification = 5

    if percentages[0,5] > threshold:
        classification = 6

    if percentages[0,6] > threshold:
        classification = 7

    return classification
