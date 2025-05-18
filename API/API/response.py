import requests

amount_of_words = 5
# http://127.0.0.1:8000/words?amount=5
response = requests.get(f'http://127.0.0.1:8000/words?amount={amount_of_words}').json()
print(response)