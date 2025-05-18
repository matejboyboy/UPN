from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import os
from functions import api
from flask_mysqldb import MySQL
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb
import re

app = Flask(__name__)
app.secret_key = '123456789'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_users'

MySQL = MySQL(app)

@app.route("/")
def home():
    completed_lessons = []
    if 'username' in session:
        username = session['username']
        cursor = MySQL.connection.cursor()
        cursor.execute("SELECT lesson_number FROM completed_lessons WHERE username = %s", (username,))
        completed_lessons = [row[0] for row in cursor.fetchall()]
        cursor.close()
    return render_template('Home.html', theme='dark', completed_lessons=completed_lessons)

@app.route("/light")
def light():
    completed_lessons = []
    if 'username' in session:
        username = session['username']
        cursor = MySQL.connection.cursor()
        cursor.execute("SELECT lesson_number FROM completed_lessons WHERE username = %s", (username,))
        completed_lessons = [row[0] for row in cursor.fetchall()]
        cursor.close()
    return render_template('HomeLight.html', theme='light', completed_lessons=completed_lessons)

@app.route("/lightlesson")
def lightLesson():
    return render_template('lightlessons.html', theme='light')

@app.route("/words", methods=['GET', 'POST'])
def words():
    return render_template('words.html', theme='dark')

@app.route('/lesson/<int:lesson_number>')
def display_lesson(lesson_number):
    file_name = str(lesson_number).zfill(3) + '.txt'
    file_path = os.path.join(os.path.dirname(__file__), 'Lessons', file_name)
    lesson_content = ""
    try:
        file = open(file_path, 'r', encoding='utf-8')
        lesson_content = file.read()
        file.close()
    except FileNotFoundError:
        lesson_content = "Error: File " + file_name + " not found in Lessons folder"
    return render_template('lesson.html', text_content=lesson_content, lesson_number=lesson_number, theme='dark')

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
    return render_template('lightlesson.html', text_content=lesson_content, lesson_number=lesson_number, theme='light')

@app.route('/gamemode')
def gamemode():
    return render_template('gamemode.html', theme='dark')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html', theme='dark')
        
        cursor = MySQL.connection.cursor()
        try:
            cursor.execute("SELECT username, password FROM tbl_users WHERE username = %s", (username,))
            user = cursor.fetchone()
        except Exception as e:
            cursor.close()
            flash('An error occurred. Please try again later.', 'error')
            return render_template('login.html', theme='dark')
        finally:
            cursor.close()
        
        if user is None:
            flash('error wrong username', 'error')
            return render_template('login.html', theme='dark')
        elif not check_password_hash(user[1], password):
            flash('error wrong password', 'error')
            return render_template('login.html', theme='dark')
        else:
            session['username'] = user[0]
            return redirect(url_for('home'))
        
    return render_template('login.html', theme='dark')

@app.route('/lightlogin', methods=['GET', 'POST'])
def lightlogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('loginLight.html', theme='light')
        
        cursor = MySQL.connection.cursor()
        try:
            cursor.execute("SELECT username, password FROM tbl_users WHERE username = %s", (username,))
            user = cursor.fetchone()
        except Exception as e:
            cursor.close()
            flash('An error occurred. Please try again later.', 'error')
            return render_template('loginLight.html', theme='light')
        finally:
            cursor.close()
        
        if user is None:
            flash('error wrong username', 'error')
            return render_template('loginLight.html', theme='light')
        elif not check_password_hash(user[1], password):
            flash('error wrong password', 'error')
            return render_template('loginLight.html', theme='light')
        else:
            session['username'] = user[0]
            return redirect(url_for('light'))
        
    return render_template('loginLight.html', theme='light')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        registration_date = date.today()
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('register.html', username=username, theme='dark')
        
        cursor = MySQL.connection.cursor()
        try:
            cursor.execute("SELECT username FROM tbl_users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('Username already exists.', 'error')
                return render_template('register.html', username=username, theme='dark')
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO tbl_users (username, password, registration_date) VALUES (%s, %s, %s)", 
                          (username, hashed_password, registration_date))
            MySQL.connection.commit()
        except MySQLdb.Error as e:
            MySQL.connection.rollback()
            flash(f'Database error: {str(e)}', 'error')
            return render_template('register.html', username=username, theme='dark')
        finally:
            cursor.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', theme='dark')

@app.route('/lightregister', methods=['GET', 'POST'])
def lightregister():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        registration_date = date.today()
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('registerLight.html', username=username, theme='light')
        
        cursor = MySQL.connection.cursor()
        try:
            cursor.execute("SELECT username FROM tbl_users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('Username already exists.', 'error')
                return render_template('registerLight.html', username=username, theme='light')
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO tbl_users (username, password, registration_date) VALUES (%s, %s, %s)", 
                          (username, hashed_password, registration_date))
            MySQL.connection.commit()
        except MySQLdb.Error as e:
            MySQL.connection.rollback()
            flash(f'Database error: {str(e)}', 'error')
            return render_template('registerLight.html', username=username, theme='light')
        finally:
            cursor.close()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('lightlogin'))
    
    return render_template('registerLight.html', theme='light')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    cur = MySQL.connection.cursor()
    cur.execute("SELECT registration_date FROM tbl_users WHERE username = %s", (username,))
    user_data = cur.fetchone()
    cur.execute("SELECT COUNT(*) FROM completed_lessons WHERE username = %s", (username,))
    completed_count = cur.fetchone()[0]
    cur.close()
    join_date = user_data[0].strftime('%B %d, %Y') if user_data else "Unknown"
    return render_template('profile.html', username=username, join_date=join_date, completed_count=completed_count, theme='dark')

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
    return render_template('profileLight.html', username=username, join_date=join_date, theme='light')

@app.route('/api')
def api_endpoint_ajax():
    amount = int(request.args.get('amount'))
    words = api(amount)
    return words

@app.route('/complete_lesson/<int:lesson_number>', methods=['POST'])
def complete_lesson(lesson_number):
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    username = session['username']
    cursor = MySQL.connection.cursor()
    try:
        cursor.execute("INSERT INTO completed_lessons (username, lesson_number) VALUES (%s, %s)", (username, lesson_number))
        MySQL.connection.commit()
    except MySQLdb.IntegrityError:
        # Lesson already completed, no action needed
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
    cursor.execute("""
        SELECT username, COUNT(lesson_number) as lesson_count
        FROM completed_lessons
        GROUP BY username
        ORDER BY lesson_count DESC
    """)
    leaders = cursor.fetchall()
    cursor.close()
    return render_template('leaderboard.html', leaders=leaders)

@app.route('/leaderboardLight')
def leaderboardLight():
    cursor = MySQL.connection.cursor()
    cursor.execute("""
        SELECT username, COUNT(lesson_number) as lesson_count
        FROM completed_lessons
        GROUP BY username
        ORDER BY lesson_count DESC
    """)
    leaders = cursor.fetchall()
    cursor.close()
    return render_template('leaderboardLight.html', leaders=leaders)



app.run(debug=True, port=8080) 