FROM ubuntu:22.04
MAINTAINER basisushil@gmail.com

RUN apt-get update -y
RUN apt-get install python3-pip -y
RUN apt-get install gunicorn3 -y


COPY requirements.txt requirements.txt
COPY . /opt/

ENV EMBEDDER_MODEL="bert-base-nli-mean-tokens"

RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader wordnet
RUN python3 -c 'from sentence_transformers import SentenceTransformer; import os; os.environ["EMBEDDER_MODEL"] = "bert-base-nli-mean-tokens"; model = SentenceTransformer(os.environ["EMBEDDER_MODEL"])'


#RUN python3 -c 'from sentence_transformers import SentenceTransformer; model = SentenceTransformer("bert-base-nli-mean-tokens")'

WORKDIR /opt/


CMD ["gunicorn3", "-b", "0.0.0.0:8000", "main:app", "--workers=5"]