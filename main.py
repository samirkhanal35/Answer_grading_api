from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource
from sentence_transformers import SentenceTransformer
import os
# importing grader
from grader import get_marks

app = Flask(__name__)
api = Api(app)


embedder_model = os.environ.get("EMBEDDER_MODEL", "default_model_name")
model = SentenceTransformer(embedder_model)

# Importing the tokenizer
# print('0---Startef000000')
# import time
# time.sleep(10)
# print()
# model = SentenceTransformer('bert-base-nli-mean-tokens')
# time.sleep(60)
print('0---Stop---------------')

# Create a simple data store for questions and answers
data_store = {
    'question': '',
    'answer': '',
    'fullmarks': 0,
    'context': ''
}

parser = reqparse.RequestParser()

# adding parser arguments
parser.add_argument('question')
parser.add_argument('answer')


# Returns the marks
class Grader_(Resource):
    def get(self):
        data = request.get_json()
        data_store['question'] = data.get('question', '')
        data_store['answer'] = data.get('answer', '')
        data_store['context'] = data.get('context', '')
        data_store['fullmarks'] = data.get('fullmarks', '')
        marks = get_marks(data_store['question'], data_store['answer'],
                          data_store['context'], data_store['fullmarks'], model)
        return {'marks': marks}


# Api resource routing
api.add_resource(Grader_, '/')


if __name__ == '__main__':
    app.run(debug=True)
