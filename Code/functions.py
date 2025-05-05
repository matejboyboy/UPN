from flask import request
import json
import requests

def generated_words(word_count):
    api_url = f'https://random-word-api.herokuapp.com/word?number={word_count}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # error ce 4xx alpa 5xx

        words = json.loads(response.text)  # json u py list
        if isinstance(words, list):
            return words
        else:
            raise ValueError("Expected a list in the JSON response.")
    except (requests.RequestException, json.JSONDecodeError, ValueError) as e:
        print("Error:", e)
        return []

