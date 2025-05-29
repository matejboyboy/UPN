from flask import request
import json
import requests

def api(amount_of_words):
    # http://127.0.0.1:8000/words?amount=5
    response = requests.get(f'http://127.0.0.1:8000/words?amount={amount_of_words}').json()
    dict = response
    # lst = []
    words = ''
    amount_of_words_str = str(amount_of_words)
    for i in range(amount_of_words):
        value = dict[amount_of_words_str][i]
        value = value + ' '
        words = words + value
    return words
api(5)