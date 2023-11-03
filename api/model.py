# import required libraries
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

stop_words = set(stopwords.words('english'))

from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer

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
   