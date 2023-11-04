from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

# importing grader
from grader import get_marks

app = Flask(__name__)
api = Api(app)


# Create a simple data store for questions and answers
data_store = {
    'question': '',
    'answer': ''
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
        marks = get_marks(data_store['question'], data_store['answer'])
        return {'marks': marks}

    


## Api resource routing 
api.add_resource(Grader_, '/')



if __name__ == '__main__':
    app.run(debug=True)