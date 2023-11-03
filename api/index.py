from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scraper import  scrape
fullmarks = 5
import re
import nltk
# nltk.download('punkt')
import tensorflow_hub as hub
# nltk.download('wordnet')
# nltk.download('stopwords')
from nltk.corpus import stopwords

import requests
from bs4 import BeautifulSoup

stop_words = set(stopwords.words('english'))

from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer


app = Flask(__name__)

# Functions
def preprocess_text(text):
    # convert to lowercase
    text = text.lower()
    
    # remove punctuation and digits
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    # remove stopwords and lemmatize
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    text = ' '.join(tokens)
    return text

def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

def calculate_relevance(desired_answer: str, student_answer: str) -> float:
    lemmatizer = WordNetLemmatizer()
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    desired_answer = preprocess_text(desired_answer)
    student_answer = preprocess_text(student_answer)
    # print("preprocessed desired answer: ", desired_answer)

    # compute cosine similarity between desired_answer and student_answer texts
    similarity = cosine(model.encode(desired_answer), model.encode(student_answer))
    return similarity

def get_marks(question: str, answer: str)-> float:
    reference_answers = scrape(question)
    marks = []
    if reference_answers:
        for each_answer in reference_answers:
            tmpmrk = calculate_relevance(each_answer, answer)
            marks.append(round(tmpmrk*fullmarks))
    return((sum(marks)/len(marks)))

def scrape(question: str)-> list:
    # removing question mark from the text
    txt = question.split('?')

    # changing the text to query format
    tmp_search_txt = ''
    for each in txt:
        if each:
            tmp_search_txt+= each 
    search_txt = ''
    for each in tmp_search_txt.split():
        search_txt+=each+'+'
    search_txt = search_txt[:-1]

    # Urls
    urls = []
    url1 = 'https://www.google.com/search?q='+search_txt
    urls.append(url1)
    url2 = 'https://www.bing.com/search?q='+search_txt
    urls.append(url2)

    contents = []

    for e_url in urls:
        try:
            # Send an HTTP GET request to the URL
            response = requests.get(e_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the page content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                text_content = soup.get_text()
                contents.append(text_content)
        except:
            pass

    return contents

@app.route("/", methods=["GET"])
def hello():
    question = 'What Is Image Transform?'
    answer = 'An image can be expanded in terms of a discrete set of basis arrays called basis images. Hence, these basis images can be generated by unitary matrices. An NxN image can be viewed as an N^2×1 vector. It provides a set of coordinates or basis vectors for vector space.'
    marks = get_marks(question, answer)
    return jsonify(" Marks: " + str(marks))




