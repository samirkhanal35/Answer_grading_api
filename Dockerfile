FROM python:3.9.12

ENV WORKDIR=/Answer_grading_api
ENV PATH=$PATH:$WORKDIR/ans/bin
WORKDIR $WORKDIR
ENV PATH=$PATH:/ans/bin

COPY /*.py $WORKDIR/
COPY main.py requirements.txt $WORKDIR/

# Create environment
RUN python -m venv ans &&\ 
    chmod -R 755 $WORKDIR/ &&\
    ans/bin/activate &&\
    ans/bin/pip install --upgrade pip &&\
    ans/bin/pip install --no-cache-dir --upgrade -r requirements.txt && \
    ans/bin/python -m nltk.downloader stopwords

CMD uvicorn main:app --host 0.0.0.0 --port 80
