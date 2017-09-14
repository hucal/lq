from requests import get
from bs4 import BeautifulSoup

url = 'https://api.stackexchange.com'

question_query = url + """/2.2/questions?pagesize=100&order=desc&sort=votes&tagged={}&site=stackoverflow&filter=!9YdnSEcyO"""

# No more than 5 tags at a time
tags = ';'.join(['c'])

response = get(question_query.format(tags))
response_json = response.json()

accepted = [i for i in response_json.get('items', []) if 'accepted_answer_id' in i]

answer_ids = [str(answer['accepted_answer_id']) 
        for answer in accepted]

# No more than 100 answer IDs at a time
answer_ids = answer_ids[0:100]

# Use this interface to edit the filter: 
# https://api.stackexchange.com/docs/answers-by-ids#order=desc&sort=activity&ids=46227775%3B45875328&filter=!b0OfNQNp_7NpC*&site=stackoverflow&run=true
answers_query = url + """/2.2/answers/{}?pagesize=30&order=desc&sort=votes&site=stackoverflow&filter=!b0OfNQNp_7NpC*"""

answer_response = get(answers_query.format(';'.join(answer_ids)))

answer_response_json = answer_response.json()
answer_bodies = [(a['body'], a['answer_id']) 
        for a in answer_response_json.get('items', [])
        if 'body' in a]

soups = [(BeautifulSoup(a, "lxml"), i)
        for a, i in answer_bodies] 

# use findAll
answer_code = [(tag.text, i)
        for (soup, i) in soups
        for tag in soup.findAll('pre') 
        ]

import pprint
pprint.pprint(answer_code)
