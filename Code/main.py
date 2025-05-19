from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import os
from functions import api
from flask_mysqldb import MySQL
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb

app = Flask(__name__)  # Creates a Flask application instance
app.secret_key = '123456789'  # Sets a secret key for session management and flashing (insecure, should be random in production)

app.config['MYSQL_HOST'] = 'localhost'  # Configures MySQL host to localhost
app.config['MYSQL_USER'] = 'root'  # Sets MySQL username to root
app.config['MYSQL_PASSWORD'] = ''  # Sets MySQL password to empty (insecure, should be set in production)
app.config['MYSQL_DB'] = 'flask_users'  # Specifies the database name as flask_users

MySQL = MySQL(app)  # Initializes MySQL extension with the Flask app

@app.route("/")  
def home():  
    completed_lessons = []  
    if 'username' in session: 
        username = session['username']  
        cursor = MySQL.connection.cursor()  
        cursor.execute("SELECT lesson_number FROM completed_lessons WHERE username = %s", (username,))  
        completed_lessons = [row[0] for row in cursor.fetchall()]  
        cursor.close()  
    return render_template('Home.html', completed_lessons=completed_lessons)  

@app.route("/light")  
def light():
    completed_lessons = []   
    if 'username' in session:  
        username = session['username']  
        cursor = MySQL.connection.cursor()  
        cursor.execute("SELECT lesson_number FROM completed_lessons WHERE username = %s", (username,))  
        completed_lessons = [row[0] for row in cursor.fetchall()]  
        cursor.close()  
    return render_template('HomeLight.html', completed_lessons=completed_lessons)  

@app.route("/lightlesson")  
def lightLesson():  
    return render_template('lightlessons.html')  

@app.route("/words", methods=['GET', 'POST'])  
def words():  
    return render_template('words.html')

@app.route('/lesson/<int:lesson_number>') 
def display_lesson(lesson_number):  
    file_name = str(lesson_number).zfill(3) + '.txt'  # Creates filename with padded lesson number (e.g., 001.txt)
    file_path = os.path.join(os.path.dirname(__file__), 'Lessons', file_name)  # Builds path to lesson file
    lesson_content = ""  # Initializes empty string for lesson content
    try:  # Attempts to read the lesson file
        file = open(file_path, 'r', encoding='utf-8')  # Opens file in read mode with UTF-8 encoding
        lesson_content = file.read()  # Reads entire file content
        file.close()  # Closes the file
    except FileNotFoundError:  # Handles case where file is not found
        lesson_content = "Error: File " + file_name + " not found in Lessons folder"  # Sets error message
    return render_template('lesson.html', text_content=lesson_content, lesson_number=lesson_number)  # Renders lesson.html with content and number

@app.route('/lightlesson/<int:lesson_number>') 
def display_lightlesson(lesson_number):  
    file_name = str(lesson_number).zfill(3) + '.txt'  
    file_path = os.path.join(os.path.dirname(__file__), 'Lessons', file_name)  
    lesson_content = "" 
    try:
        file = open(file_path, 'r', encoding='utf-8')
        lesson_content = file.read()
        file.close()
    except FileNotFoundError:
        lesson_content = "Error: File " + file_name + " not found in Lessons folder"
    return render_template('lightlesson.html', text_content=lesson_content, lesson_number=lesson_number)

@app.route('/gamemode')
def gamemode():
    return render_template('gamemode.html')
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')  # Gets username from form
        password = request.form.get('password')  # Gets password from form
        if not username or not password:  # Checks if fields are empty
            flash('Username and password are required.', 'error')  # Flashes error message
            return render_template('login.html')
        cursor = MySQL.connection.cursor()  # Creates database cursor
        try:
            cursor.execute("SELECT username, password FROM tbl_users WHERE username = %s", (username,))  # Queries user data
            user = cursor.fetchone()  # Fetches user record
        except Exception as e:  # Handles database errors
            cursor.close()  # Closes cursor
            flash('An error occurred. Please try again later.', 'error')  # Flashes error
            return render_template('login.html')
        finally:  # Ensures cursor is closed
            cursor.close()  # Closes cursor
        if user is None:  # Checks if user doesn’t exist
            flash('error wrong username', 'error')  # Flashes error
            return render_template('login.html')
        elif not check_password_hash(user[1], password):  # Checks password hash
            flash('error wrong password', 'error')  # Flashes error
            return render_template('login.html')  # Renders login.html
        else:  # Successful login
            session['username'] = user[0]  # Stores username in session
            return redirect(url_for('home'))  # Redirects to homepage
    return render_template('login.html')

@app.route('/lightlogin', methods=['GET', 'POST'])
def lightlogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('loginLight.html')
        cursor = MySQL.connection.cursor()
        try:
            cursor.execute("SELECT username, password FROM tbl_users WHERE username = %s", (username,))
            user = cursor.fetchone()
        except Exception as e:
            cursor.close()
            flash('An error occurred. Please try again later.', 'error')
            return render_template('loginLight.html')
        finally:
            cursor.close()
        if user is None:
            flash('error wrong username', 'error')
            return render_template('loginLight.html')
        elif not check_password_hash(user[1], password):
            flash('error wrong password', 'error')
            return render_template('loginLight.html')
        else:
            session['username'] = user[0]
            return redirect(url_for('light'))
    return render_template('loginLight.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')  # Gets username
        password = request.form.get('password')  # Gets password
        registration_date = date.today()  # Gets current date
        if not username or not password:  # Checks for empty fields
            flash('Username and password are required.', 'error')  # Flashes error
            return render_template('register.html', username=username)
        cursor = MySQL.connection.cursor()  # Creates cursor
        try:
            cursor.execute("SELECT username FROM tbl_users WHERE username = %s", (username,))  # Checks if username exists
            if cursor.fetchone():  # If username exists
                flash('Username already exists.', 'error')  # Flashes error
                return render_template('register.html', username=username)
            hashed_password = generate_password_hash(password)  # Hashes password
            cursor.execute("INSERT INTO tbl_users (username, password, registration_date) VALUES (%s, %s, %s)", 
                          (username, hashed_password, registration_date))  # Inserts new user
            MySQL.connection.commit()  # Commits transaction
        except MySQLdb.Error as e:  # Handles database errors
            MySQL.connection.rollback()  # Rolls back transaction
            flash(f'Database error: {str(e)}', 'error')  # Flashes error
            return render_template('register.html', username=username)
        finally:  # Ensures cursor is closed
            cursor.close()  # Closes cursor
        flash('Registration successful! Please log in.', 'success')  # Flashes success message
        return redirect(url_for('login'))  # Redirects to login
    return render_template('register.html')

@app.route('/lightregister', methods=['GET', 'POST'])
def lightregister():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        registration_date = date.today()
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('registerLight.html', username=username)
        cursor = MySQL.connection.cursor()
        try:
            cursor.execute("SELECT username FROM tbl_users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('Username already exists.', 'error')
                return render_template('registerLight.html', username=username)
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO tbl_users (username, password, registration_date) VALUES (%s, %s, %s)", 
                          (username, hashed_password, registration_date))
            MySQL.connection.commit()
        except MySQLdb.Error as e:
            MySQL.connection.rollback()
            flash(f'Database error: {str(e)}', 'error')
            return render_template('registerLight.html', username=username)
        finally:
            cursor.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('lightlogin'))
    return render_template('registerLight.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Removes username from session
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' not in session:  # Checks if user is logged in
        return redirect(url_for('login'))
    username = session['username']  # Gets username from session
    cur = MySQL.connection.cursor()
    cur.execute("SELECT registration_date FROM tbl_users WHERE username = %s", (username,))  # Queries registration date
    user_data = cur.fetchone()  # Fetches user data
    cur.execute("SELECT COUNT(*) FROM completed_lessons WHERE username = %s", (username,))  # Counts completed lessons
    completed_count = cur.fetchone()[0]  # Gets lesson count
    cur.close()
    join_date = user_data[0].strftime('%B %d, %Y') if user_data else "Unknown"  # Formats join date
    return render_template('profile.html', username=username, join_date=join_date, completed_count=completed_count)

@app.route('/lightprofile')
def lightprofile():
    if 'username' not in session:
        return redirect(url_for('lightlogin'))
    username = session['username']
    cur = MySQL.connection.cursor()
    cur.execute("SELECT registration_date FROM tbl_users WHERE username = %s", (username,))
    user_data = cur.fetchone()
    cur.close()
    join_date = user_data[0].strftime('%B %d, %Y') if user_data else "Unknown"
    return render_template('profileLight.html', username=username, join_date=join_date)

@app.route('/api')
def api_endpoint_ajax():
    amount = int(request.args.get('amount'))
    words = api(amount)
    return words

@app.route('/complete_lesson/<int:lesson_number>', methods=['POST'])  # Defines route to mark lesson completion
def complete_lesson(lesson_number):
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    username = session['username']
    cursor = MySQL.connection.cursor()
    try:
        cursor.execute("INSERT INTO completed_lessons (username, lesson_number) VALUES (%s, %s)", (username, lesson_number))  # Inserts lesson completion
        MySQL.connection.commit()
    except MySQLdb.IntegrityError:
        pass
    except Exception as e:
        MySQL.connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
    return jsonify({'success': True})

@app.route('/leaderboard')
def leaderboard():
    cursor = MySQL.connection.cursor()
    cursor.execute("""  # Executes query to get leaderboard data
        SELECT username, COUNT(lesson_number) as lesson_count
        FROM completed_lessons
        GROUP BY username
        ORDER BY lesson_count DESC
    """)
    leaders = cursor.fetchall()  # Fetches leaderboard data
    cursor.close()
    return render_template('leaderboard.html', leaders=leaders)

@app.route('/leaderboardLight')
def leaderboardLight():
    cursor = MySQL.connection.cursor()
    cursor.execute("""  # Queries leaderboard data
        SELECT username, COUNT(lesson_number) as lesson_count
        FROM completed_lessons
        GROUP BY username
        ORDER BY lesson_count DESC
    """)
    leaders = cursor.fetchall() 
    cursor.close() 
    return render_template('leaderboardLight.html', leaders=leaders)

app.run(debug=True, port=8080)
