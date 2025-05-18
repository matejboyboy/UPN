from fastapi import FastAPI
from openFile import opentxt
import random

app = FastAPI()



# @app.get('/items')
# def get(age: int, sex:str):
#     if age<15 or sex == 'F':
#         return {'survived' : 1}
#     else:
#         return {'survived' : 0}
    
@app.get('/')
def get():
    return {'hello' : 'there'}
    
indexes = []

@app.get('/words')
def get(amount: int):
    indexes.clear()
    content = opentxt('1kWORDS.txt')
    indexes.extend(content.splitlines())

    selected_words = []
    for x in range(amount):
        random_word = random.choice(indexes)
        selected_words.append(random_word)
    return {amount : selected_words}
