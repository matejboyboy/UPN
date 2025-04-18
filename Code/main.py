from flask import Flask, render_template, request, jsonify
import threading
from functions import generated_words



app = Flask(__name__)



@app.route("/",)
def hello_world():
    return render_template('index.html')

# @app.route("/submitted", methods = ['POST', 'GET'])
# def submitted():
#     tip = type(user_input).__name__
#     return render_template("index.html")





@app.route("/words", methods=['GET', 'POST'])
def test():
    parsed_words = ""
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

# @app.route("/words")
# def words():
#     return render_template('words.html', )


app.run(debug = True)