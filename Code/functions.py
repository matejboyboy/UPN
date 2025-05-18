from flask import request
import json
import requests

# def generated_words(word_count):
#     api_url = f'https://random-word-api.herokuapp.com/word?number={word_count}'

#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()  # error ce 4xx alpa 5xx

#         words = json.loads(response.text)  # json u py list
#         if isinstance(words, list):
#             return words
#         else:
#             raise ValueError("Expected a list in the JSON response.")
#     except (requests.RequestException, json.JSONDecodeError, ValueError) as e:
#         print("Error:", e)
#         return []

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