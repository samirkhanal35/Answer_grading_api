
FROM python:3.9.6
MAINTAINER basisushil@gmail.com

WORKDIR /opt/
ENV DOCKER_DEFAULT_PLATFORM=linux/amd64

COPY *.py .
COPY requirements.txt ./requirements.txt

ENV EMBEDDER_MODEL="bert-base-nli-mean-tokens"

RUN apt-get update -y && \
    python -m venv ./venv &&\
    chmod -R 755 . &&\
    ./venv/bin/activate &&\
    ./venv/bin/pip install -r requirements.txt &&\
    ./venv/bin/python -m nltk.downloader stopwords &&\
    ./venv/bin/python -m nltk.downloader punkt &&\
    ./venv/bin/python -m nltk.downloader wordnet &&\
    ./venv/bin/python -c 'from sentence_transformers import SentenceTransformer; import os; os.environ["EMBEDDER_MODEL"] = "bert-base-nli-mean-tokens"; model = SentenceTransformer(os.environ["EMBEDDER_MODEL"])'

#RUN python3 -c 'from sentence_transformers import SentenceTransformer; model = SentenceTransformer("bert-base-nli-mean-tokens")'

CMD ./venv/bin/gunicorn -b 0.0.0.0:8000 main:app --workers=5