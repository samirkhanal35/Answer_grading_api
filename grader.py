# import required libraries
from sentence_transformers import SentenceTransformer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import tensorflow_hub as hub
import nltk
import re
import pandas as pd
import numpy as np


# import scraper
from scraper import scrape

# Setting the fullmarks as 5
fullmarks = 5

# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')

# getting only english stopwords
stop_words = set(stopwords.words('english'))


# Defining WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


def preprocess_text(text):
    # convert to lowercase
    text = text.lower()

    # remove punctuation and digits
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    # remove stopwords and lemmatize
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token)
              for token in tokens if token not in stop_words]
    text = ' '.join(tokens)
    return text


# Importing the tokenizer
model = SentenceTransformer('bert-base-nli-mean-tokens')

# Calculate cosine similarity


def cosine(u, v):
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

# calculate the relevance


def calculate_relevance(desired_answer: str, student_answer: str):
    desired_answer = preprocess_text(desired_answer)
    student_answer = preprocess_text(student_answer)
    # print("preprocessed desired answer: ", desired_answer)

    # compute cosine similarity between desired_answer and student_answer texts
    similarity = cosine(model.encode(desired_answer),
                        model.encode(student_answer))
    return similarity

# main function


def get_marks(question: str, answer: str):
    ''' Returns the average marks '''
    reference_answers = scrape(question)
    marks = []
    if reference_answers:
        for each_answer in reference_answers:
            tmpmrk = calculate_relevance(each_answer, answer)
            marks.append(round(tmpmrk*fullmarks))
    return ((sum(marks)/len(marks)))
