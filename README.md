# API For Short Answer Grading
This is an Flask API for Short Answer Grading. It takes input as question, students answer, question fullmarks, and the context or reference answer. <br/>
<br/>
The questions are used to scrape the answers from google and bing. The scraped answers are used as reference answers. The similarity betweent the students answer and the reference answers including the passed reference answer is calculated using cosine similarity, averaged it and sent back as response.


Requirements:
Python3, Flask, flask_restful, request, bs4(beautiful soup)


API Call:
url: 'http://localhost/'
request type: GET
json_format: {
    'question': '',
    'answer': '',
    'fullmarks': 0,
    'context': ''
}
