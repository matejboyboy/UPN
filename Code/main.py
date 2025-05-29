from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import os
from functions import api
from flask_mysqldb import MySQL
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
import MySQLdb
import random

app = Flask(__name__)
# Secret key za Flask namnjen da se podatkov ne da spremenijat.
app.secret_key = '123456789'

# Konfiguracija povezave z MySQL bazo podatkov.
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_users'

MySQL = MySQL(app)  # Poveže Flask z SQL bazo.

# Dovoljene poti do profilnih slik.
ALLOWED_PROFILE_PICTURES = [
    '/static/Slike/PIG.png',
    '/static/Slike/FROG.png', 
    '/static/Slike/TIGER.png',
    '/static/Slike/BEAR.png'
]

PROGRAMMING_LESSONS = {
    'C++': {'base': 107, 'count': 5},
    'CSS': {'base': 112, 'count': 5},
    'HTML': {'base': 117, 'count': 5},
    'JavaScript': {'base': 122, 'count': 5},
    'Python': {'base': 127, 'count': 5}
}

@app.route("/")
def home():
    if 'username' in session: # Preveri ali obstaja uporabniško ime v sessinu.
        username = session['username'] # Pridobi uporabniško ime iz sessina.
        cursor = MySQL.connection.cursor() # Ustvari povezavo za izvajanje poizvedb v bazi
        cursor.execute("UPDATE tbl_users SET theme_preference = 'dark' WHERE username = %s", (username,)) # Preverimo ali ima uporabnik že izbrano temo ter jo posodobimo na dark.
        MySQL.connection.commit() # Comitas spremembe v bazi.
        cursor.execute("SELECT lesson_number FROM completed_lessons WHERE username = %s", (username,)) # Naredimo poizvedbo da izvemo kere lessone je naredil uporabnik.
        completed_lessons = [row[0] for row in cursor.fetchall()] # Rezultate pretvori v seznam številk lessenov.
        cursor.close() # Zapremo povezavo s bazo.
    else:
        completed_lessons = [] # Naredimo prezen seznam za uporabnike ki niso loginani.
    return render_template('Home.html', completed_lessons=completed_lessons)

# Naredimo isto za light verzijo.
@app.route("/light")
def light():
    if 'username' in session:
        username = session['username']
        cursor = MySQL.connection.cursor()
        cursor.execute("UPDATE tbl_users SET theme_preference = 'light' WHERE username = %s", (username,))
        MySQL.connection.commit()
        cursor.execute("SELECT lesson_number FROM completed_lessons WHERE username = %s", (username,))
        completed_lessons = [row[0] for row in cursor.fetchall()]
        cursor.close()
    else:
        completed_lessons = []
    return render_template('HomeLight.html', completed_lessons=completed_lessons)

@app.route("/words", methods=['GET', 'POST'])
def words():
    return render_template('words.html')

@app.route("/lightwords", methods=['GET', 'POST'])
def lightwords():
    return render_template('lightwords.html')

@app.route('/lesson/<int:lesson_number>') # Rout ustvarimo z spremenljivko lesson_number.
def display_lesson(lesson_number):
    file_name = str(lesson_number).zfill(3) + '.txt' # Ustvarimo ime datoteke, Zfill nardi da mome stevilo imet tri mesta.
    file_path = os.path.join(os.path.dirname(__file__), 'Lessons', file_name) # Sestavimo pot do lesson datoteke.
    lesson_content = "" # Ustvarmo prazen list za vsebino lessona.
    try:
        file = open(file_path, 'r', encoding='utf-8') # Odpremo datoteko za branje z UTF-8 kar omooča branje č š ž b-sa.
        lesson_content = file.read() # Prebere vsebino datoteke.
        file.close() # Zapre datoteko.
    except:
        pass
    return render_template('lesson.html', text_content=lesson_content, lesson_number=lesson_number)

# Isto samo za lihgt verzijo.
@app.route('/lightlesson/<int:lesson_number>')
def display_lightlesson(lesson_number):
    file_name = str(lesson_number).zfill(3) + '.txt'
    file_path = os.path.join(os.path.dirname(__file__), 'Lessons', file_name)
    lesson_content = ""
    try:
        file = open(file_path, 'r', encoding='utf-8')
        lesson_content = file.read()
        file.close()
    except:
        pass
    return render_template('lightlesson.html', text_content=lesson_content, lesson_number=lesson_number)

# Isto kt v lessonih sam da rount creata s pomocjo dictonarya zgorij.
@app.route('/programming_lesson/<language>')
def programming_lesson(language):
    lesson_num = random.randint(1, 5)
    base = PROGRAMMING_LESSONS[language]['base']
    file_num = base + (lesson_num - 1)
    file_name = f"{file_num:03d}{language}.txt"
    file_path = os.path.join(os.path.dirname(__file__), 'Gamemode_txt', file_name)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lesson_content = file.read().replace('\t', '    ')
    except FileNotFoundError:
        lesson_content = f"Napaka: Datoteka {file_name} ni najdena v mapi Gamemode_txt"
    return lesson_content

@app.route("/gamemode", methods=['GET', 'POST'])
def gamemode():
    if request.method == 'POST':
        pass
    else:
        return render_template('gamemode.html')

@app.route("/gamemodelight", methods=['GET', 'POST'])
def gamemodelight():
    if request.method == 'POST':
        pass
    else:
        return render_template('gamemodelight.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': # Preveri ali je POST.
        username = request.form.get('username') # Dobimo username iz obrazca.
        password = request.form.get('password') # Dobimo password iz obrazca.
        if not username or not password: # Prever če je username in password unsesena.
            flash('Uporabniško ime in geslo sta obvezna.', 'error') # Flassha error ce nista unesena.
            return render_template('login.html')
        cursor = MySQL.connection.cursor() # Nardimo povezavo s bazo.
        try:
            cursor.execute("SELECT username, password, theme_preference FROM tbl_users WHERE username = %s", (username,)) # Nardimo poizvedbo da dobimo podatke uporabnika.
            user = cursor.fetchone() # Dobimo podatke iz poizvedbe.
        except Exception as e:
            cursor.close() # Zapre povezavo med bazo in programom ob napaki.
            flash('Prišlo je do napake. Poskusite znova kasneje.', 'error') # Flasha error.
            return render_template('login.html')
        finally:
            cursor.close() # Če ni napake zapre povezavo s bazo.
        if user is None: # Pogleda če uporabnik obstaja.
            flash('napaka napačno uporabniško ime', 'error') # Flasha error če uporabnik ne obstaja.
            return render_template('login.html')
        elif not check_password_hash(user[1], password): # Pogleda če geslo obstaja.
            flash('napaka napačno geslo', 'error') # Flasha error če geslo ni pravilno ali ne obstaja.
            return render_template('login.html')
        else:
            session['username'] = user[0] # Shrani uporabniško pod session.
            theme_preference = user[2] if user[2] else 'dark' # Določi temo. Da dark če je prvi vpis.
            if theme_preference == 'light': # Preveri če je uporabnik logoutu prejsnic na svetli temi.
                return redirect(url_for('light'))
            else:
                return redirect(url_for('home'))
    return render_template('login.html')

# Ponovimo za light verzijo.
@app.route('/lightlogin', methods=['GET', 'POST'])
def lightlogin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('Uporabniško ime in geslo sta obvezna.', 'error')
            return render_template('loginLight.html')
        cursor = MySQL.connection.cursor()
        try:
            cursor.execute("SELECT username, password, theme_preference FROM tbl_users WHERE username = %s", (username,))
            user = cursor.fetchone()
        except Exception as e:
            cursor.close()
            flash('Prišlo je do napake. Poskusite znova kasneje.', 'error')
            return render_template('loginLight.html')
        finally:
            cursor.close()
        if user is None:
            flash('napaka napačno uporabniško ime', 'error')
            return render_template('loginLight.html')
        elif not check_password_hash(user[1], password):
            flash('napaka napačno geslo', 'error')
            return render_template('loginLight.html')
        else:
            session['username'] = user[0] 
            theme_preference = user[2] if user[2] else 'dark'
            if theme_preference == 'light':
                return redirect(url_for('light'))
            else:
                return redirect(url_for('home'))
    return render_template('loginLight.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        registration_date = date.today() # Dobimo se danasji datum.
        if not username or not password:
            flash('Uporabniško ime in geslo sta obvezna.', 'error')
            return render_template('register.html', username=username)
        cursor = MySQL.connection.cursor()
        try:
            cursor.execute("SELECT username FROM tbl_users WHERE username = %s", (username,))
            if cursor.fetchone(): # Preveri če uporabnik ze obstaja.
                flash('Uporabniško ime že obstaja.', 'error')
                return render_template('register.html', username=username)
            hashed_password = generate_password_hash(password) # Hasha geslo za varnost.
            cursor.execute("INSERT INTO tbl_users (username, password, registration_date, theme_preference) VALUES (%s, %s, %s, 'dark')", 
                          (username, hashed_password, registration_date)) # Vstavi podatek v bazo.
            MySQL.connection.commit() # Podatke commita.
        except MySQLdb.Error as e:
            MySQL.connection.rollback()
            flash(f'Napaka v bazi podatkov: {str(e)}', 'error')
            return render_template('register.html', username=username)
        finally:
            cursor.close()
        flash('Registracija uspešna! Prosimo, prijavite se.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Ponovimo aa light verzijo.
@app.route('/lightregister', methods=['GET', 'POST'])
def lightregister():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        registration_date = date.today()
        if not username or not password:
            flash('Uporabniško ime in geslo sta obvezna.', 'error')
            return render_template('registerLight.html', username=username)
        cursor = MySQL.connection.cursor()
        try:
            cursor.execute("SELECT username FROM tbl_users WHERE username = %s", (username,))
            if cursor.fetchone():
                flash('Uporabniško ime že obstaja.', 'error')
                return render_template('registerLight.html', username=username)
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO tbl_users (username, password, registration_date, theme_preference) VALUES (%s, %s, %s, 'light')", 
                          (username, hashed_password, registration_date))
            MySQL.connection.commit()
        except MySQLdb.Error as e:
            MySQL.connection.rollback()
            flash(f'Napaka v bazi podatkov: {str(e)}', 'error')
            return render_template('registerLight.html', username=username)
        finally:
            cursor.close()
        flash('Registracija uspešna! Prosimo, prijavite se.', 'success')
        return redirect(url_for('lightlogin'))
    return render_template('registerLight.html')

@app.route('/logout')
def logout():
    session.pop('username', None) # odstran uporabnika iz sessina.
    return redirect(url_for('login'))

# Ponovimo za light verzijo. Vem dab loh naredu za prever ker temo ma izrbano in pol te tm fukne ampak je se mi ne da.
@app.route('/logoutlight')
def logoutlight():
    session.pop('username', None)
    return redirect(url_for('lightlogin'))

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    cur = MySQL.connection.cursor()
    cur.execute("UPDATE tbl_users SET theme_preference = 'dark' WHERE username = %s", (username,))
    MySQL.connection.commit()
    cur.execute("SELECT registration_date, profile_picture FROM tbl_users WHERE username = %s", (username,)) # Naredimo poizvedbo v nasi bazi.
    user_data = cur.fetchone() # Pridobimo podatke uporabnika.
    cur.execute("SELECT COUNT(*) FROM completed_lessons WHERE username = %s", (username,)) # Prešteje koliko lessenov ma narjen.
    completed_count = cur.fetchone()[0] # Pridobimo podatke kok lessenov ma narjenih.
    cur.close()
    if user_data:
        join_date = user_data[0].strftime('%B %d, %Y') # Ustvarimo datum ki bo prikazan na profilu.
        profile_picture = user_data[1] if user_data[1] else "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y&s=80" # Ustvarimo profilno sliko če je izbrana, drgač pa sam damo privzeto sliko.
    return render_template('profile.html', username=username, join_date=join_date, completed_count=completed_count, profile_picture=profile_picture)

@app.route('/set_profile_picture', methods=['POST'])
def set_profile_picture():
    data = request.get_json() #Vrne dictinary iz pridobljenih podatkov.
    new_picture = data.get('new_picture') # Dobimo novo izbrano sliko.
    username = session['username']
    cursor = MySQL.connection.cursor()
    try:
        cursor.execute("UPDATE tbl_users SET profile_picture = %s WHERE username = %s", (new_picture, username)) # Posodobimo bazo z novo sliko.
        MySQL.connection.commit()
    except Exception as e:
        MySQL.connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
    return jsonify({'success': True, 'new_picture': new_picture})

# Ponovimo za light verzijo.
@app.route('/lightprofile')
def lightprofile():
    if 'username' not in session:
        return redirect(url_for('lightlogin'))
    username = session['username']
    cur = MySQL.connection.cursor()
    cur.execute("UPDATE tbl_users SET theme_preference = 'light' WHERE username = %s", (username,))
    MySQL.connection.commit()
    cur.execute("SELECT registration_date, profile_picture FROM tbl_users WHERE username = %s", (username,))
    user_data = cur.fetchone()
    cur.execute("SELECT COUNT(*) FROM completed_lessons WHERE username = %s", (username,))
    completed_count = cur.fetchone()[0]
    cur.close()
    if user_data:
        join_date = user_data[0].strftime('%B %d, %Y')
        profile_picture = user_data[1] if user_data[1] else "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y&s=80"
    else:
        join_date = "Neznano"
        profile_picture = "https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y&s=80"
    return render_template('profileLight.html', username=username, join_date=join_date, completed_count=completed_count, profile_picture=profile_picture)

@app.route('/remove_account', methods=['POST'])
def remove_account():
    username = session['username']
    cursor = MySQL.connection.cursor()
    try:
        cursor.execute("DELETE FROM completed_lessons WHERE username = %s", (username,)) # Izbriši lessone ki jih je naredu.
        cursor.execute("DELETE FROM tbl_users WHERE username = %s", (username,)) # Izbriše uporabnika iz baze.
        MySQL.connection.commit()
    except:
        pass
    finally:
        cursor.close()
    return jsonify({'success': True}) # Vrne da je removal acc.

@app.route('/api')
def api_endpoint_ajax():
    amount = int(request.args.get('amount')) # Dobi število besed tok kt jih je zahtevan.
    words = api(amount)
    return words

@app.route('/complete_lesson/<int:lesson_number>', methods=['POST'])
def complete_lesson(lesson_number):
    if 'username' not in session:
        return jsonify({'error': 'Ni prijavljen'}, 401) # Vrni napako če ni prijaveljen.
    username = session['username']
    cursor = MySQL.connection.cursor()
    try:
        cursor.execute("INSERT INTO completed_lessons (username, lesson_number) VALUES (%s, %s)", (username, lesson_number)) # Inserta da je lesson narjen.
        MySQL.connection.commit()
    except MySQLdb.IntegrityError:
        pass # Ignorira če je lesson že narjen.
    except Exception as e:
        MySQL.connection.rollback() # Razveljav spremembe.
        return jsonify({'error': str(e)}), 500 # Vrne error.
    finally:
        cursor.close()
    return jsonify({'success': True}) # Vrne da nardi.

@app.route('/save_score', methods=['POST'])
def save_score():
    if 'username' not in session:
        return jsonify({'error': 'ni prijavljen'}, 401)
    data = request.get_json() or {} # Pretvorimo podatke v JSON ali pa v prazni slovar če ni podatkov.
    try:
        new_wpm = int(data.get('wpm', 0)) # Dobimo wpm in ga damo v int.
        word_count = data.get('word_count') # Dobimo kok besed je uporabnik izbral.
        time_seconds = data.get('time') # Dobimo kok sekund je uporabnik izbral.
        if word_count is not None: # Preveri ali je izbral število besed.
            word_count = int(word_count) # Pretvor število besed v int.
            time_seconds = None # Nastavi čas na none saj ne moras izbrati vec vrst na enkrat.
        elif time_seconds is not None: # Ponovimo če izbere čas.
            time_seconds = int(time_seconds)
            word_count = None
        else:
            return jsonify({'error': 'mora biti podano bodisi število besed ali čas'}, 400)
    except (TypeError, ValueError) as e:
        print(f"Napaka: prejet neveljaven vnos: {data}, izjema: {str(e)}")
        return jsonify({'error': 'neveljaven vnos'}, 400)
    username = session['username']
    cursor = MySQL.connection.cursor()
    try:
        if word_count is not None:
            cursor.execute("""
                SELECT best_wpm FROM user_wpm_scores 
                WHERE username = %s AND word_count = %s AND time_seconds IS NULL
            """, (username, word_count)) # Dobimo wpm in kok besed je uporabnik izbral.
        else:
            cursor.execute("""
                SELECT best_wpm FROM user_wpm_scores 
                WHERE username = %s AND time_seconds = %s AND word_count IS NULL
            """, (username, time_seconds)) # Ponvimo a za čas. 
        row = cursor.fetchone()
        if row:
            current_best = row[0] # Pridobimo wpm userja iz baze.
            if new_wpm > current_best: # Preverimo če je nov wpm boljši of starega.
                if word_count is not None:
                    cursor.execute("""
                        UPDATE user_wpm_scores SET best_wpm = %s 
                        WHERE username = %s AND word_count = %s AND time_seconds IS NULL
                    """, (new_wpm, username, word_count)) # Vnesemo now wpm notr za tok besed.
                else:
                    cursor.execute("""
                        UPDATE user_wpm_scores SET best_wpm = %s 
                        WHERE username = %s AND time_seconds = %s AND word_count IS NULL
                    """, (new_wpm, username, time_seconds)) # Ponovimo za čas.
                updated = True # Potrdimo posodobitev.
                best = new_wpm 
            else:
                updated = False # Potrdimo da ni posodobitve.
                best = current_best
        else:
            # Ponovimo če ni wpm v bazi.
            if word_count is not None:
                cursor.execute("""
                    INSERT INTO user_wpm_scores (username, word_count, time_seconds, best_wpm) 
                    VALUES (%s, %s, NULL, %s)
                """, (username, word_count, new_wpm))
            else:
                cursor.execute("""
                    INSERT INTO user_wpm_scores (username, word_count, time_seconds, best_wpm) 
                    VALUES (%s, NULL, %s, %s)
                """, (username, time_seconds, new_wpm))
            updated = True
            best = new_wpm
        MySQL.connection.commit()
    except Exception as e:
        MySQL.connection.rollback() # Razveljavimo spremembe če je napake.
        print(f"Napaka v bazi podatkov v save_score: {str(e)}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
    return jsonify({'updated': updated, 'best_wpm': best})

@app.route('/leaderboard')
def leaderboard():
    category = request.args.get('category', 'classes') # Iz vrste leaderboarda ki ga izberemo dobimo vn kategorijo.
    cur = MySQL.connection.cursor()
    if category == 'classes': # Preveri ce je katogorija classes.
        cur.execute("""
            SELECT u.username, COUNT(c.lesson_number) AS lesson_count FROM tbl_users AS u
                LEFT JOIN completed_lessons AS c ON u.username = c.username
            GROUP BY u.username
            ORDER BY lesson_count DESC
        """) # Nardimo poizvebo ki razvrsti uporabnike po kok lessonnov majo narejnih.
        leaders = cur.fetchall()  # Dobimo vse rezultate poizvedbe.
        header = "Največ dokončanih lekcij"  # Natav naslov columa.
    elif category.startswith('wpm'): # Prever a se začne kategorija z wpm.
        try:
            word_count = int(category[3:]) # Pretvor število besed v int.
        except ValueError:
            return "Neveljavna kategorija", 400 # Vrne error ce ni stevilo vrsta kategorije.
        cur.execute("""
            SELECT u.username, COALESCE(s.best_wpm, 0) AS best_wpm FROM tbl_users u
                LEFT JOIN user_wpm_scores s ON u.username = s.username AND s.word_count = %s AND s.time_seconds IS NULL
            ORDER BY best_wpm DESC
        """, (word_count,)) # Naredimo poizvedbo za ratvrstitev userjev po wpm za doloceno kategorijo besed.
        leaders = cur.fetchall() # Pridobimo razultate.
        header = f"Najboljši WPM za {word_count} besed" # Nastav naslov columa.
    # Ponovimo za time kategorijo.
    elif category.startswith('time'):
        try:
            time_seconds = int(category[4:])  * 1000 # Pretvori čas v celo int.
        except ValueError:
            return "Neveljavna kategorija", 400
        cur.execute("""
            SELECT u.username, COALESCE(s.best_wpm, 0) AS best_wpm FROM tbl_users u
                LEFT JOIN user_wpm_scores s ON u.username = s.username AND s.time_seconds = %s AND s.word_count IS NULL
            ORDER BY best_wpm DESC
        """, (time_seconds,))
        leaders = cur.fetchall()
        header = f"Najboljši WPM v {time_seconds} sekundah"
    else:
        return "Neveljavna kategorija", 400
    cur.close()
    return render_template('leaderboard.html', leaders=leaders, category=category, header=header)

# Ponovimo za light verzijo.
@app.route('/leaderboardLight')
def leaderboardLight():
    category = request.args.get('category', 'classes')
    cur = MySQL.connection.cursor()
    if category == 'classes':
        cur.execute("""
            SELECT u.username, COUNT(c.lesson_number) AS lesson_count FROM tbl_users AS u
                LEFT JOIN completed_lessons AS c ON u.username = c.username
            GROUP BY u.username
            ORDER BY lesson_count DESC
        """)
        leaders = cur.fetchall()
        header = "Največ dokončanih lekcij"
    elif category.startswith('wpm'):
        try:
            word_count = int(category[3:])
        except ValueError:
            return "Neveljavna kategorija", 400
        cur.execute("""
            SELECT u.username, COALESCE(s.best_wpm, 0) AS best_wpm FROM tbl_users u
                LEFT JOIN user_wpm_scores s ON u.username = s.username AND s.word_count = %s AND s.time_seconds IS NULL
            ORDER BY best_wpm DESC
        """, (word_count,))
        leaders = cur.fetchall()
        header = f"Najboljši WPM za {word_count} besed"
    elif category.startswith('time'):
        try:
            time_seconds = int(category[4:]) * 1000  # Convert seconds to milliseconds
        except ValueError:
            return "Neveljavna kategorija", 400
        cur.execute("""
            SELECT u.username, COALESCE(s.best_wpm, 0) AS best_wpm FROM tbl_users u
                LEFT JOIN user_wpm_scores s ON u.username = s.username AND s.time_seconds = %s AND s.word_count IS NULL
            ORDER BY best_wpm DESC
        """, (time_seconds,))
        leaders = cur.fetchall()
        header = f"Najboljši WPM v {time_seconds // 1000} sekundah"  # Display in seconds
    else:
        return "Neveljavna kategorija", 400
    cur.close()
    return render_template('leaderboardLight.html', leaders=leaders, category=category, header=header)

if __name__ == '__main__':
    app.run(debug=True, port=8080)