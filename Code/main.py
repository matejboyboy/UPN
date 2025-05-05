from flask import Flask, render_template, request, jsonify, redirect
import threading
from functions import generated_words
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route("/word_count",)
def wordCount():
    return render_template('index.html')

@app.route("/words", methods=['GET', 'POST'])
def freeType(): 
    parsed_words = "" #iz formata k ti ga vrne api, ti da samo besede, k se pol shranjo pod word var in se pol z jinja printa na html
    counter = 0
    if request.method == 'POST': 
        user_input = request.form['user_text']
        word_list = generated_words(int(user_input))
        for word in word_list:
            if counter == 0:
                parsed_words = parsed_words + word
                counter += 1
            else:
                parsed_words = parsed_words + " " + word
        return render_template('words.html', word = parsed_words)


#rout do lessona in stevilo postane spremenljivka lesson_number
@app.route('/lesson/<int:lesson_number>')
def display_lesson(lesson_number):
    #zfill(3) rabis zato da naredi file name "001" namesto "1"
    file_name = str(lesson_number).zfill(3) + '.txt'
    #Naredi pot to fijla (.join zduzi vec poti), (dirname vrne pot do trenutne mape, (__file__ je trenut datoteka), ki jo odstrani iz routa, doda Lessons v route in se file_name
    file_path = os.path.join(os.path.dirname(__file__), 'Lessons', file_name)
    # print(file_path)
    lesson_content = ""
    try:
        #Odpre file ter ga prebere in shrani text v fijlu pod lesson_content in zapre file, utf-8 za č
        file = open(file_path, 'r', encoding='utf-8')
        lesson_content = file.read()
        file.close()
    
    except FileNotFoundError:
        lesson_content = "Error: File " + file_name + " not found in Lessons folder"
    return render_template('lesson.html', text_content=lesson_content)

app.run(debug = True, port=5000)