from flask import Flask, request, session, redirect
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt


app = Flask(__name__)

app.secret_key = 'some_secret'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3301
app.config['MYSQL_USER'] = 'flask'
app.config['MYSQL_PASSWORD'] = 'ksalf'
app.config['MYSQL_DB'] = 'social_network'
 
mysql = MySQL(app)


@app.route("/register", methods = ['POST'])
def register():
    data = request.get_json()
    login, password = data["login"], data["password"]
    if login and password:
        password_hash = sha256_crypt.encrypt(password)
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO users(login, password) VALUES(%s,%s)''',\
            (login, password_hash))
        mysql.connection.commit()
        cursor.close()
        return "ok", 200


@app.route("/login", methods = ['POST'])
def login():
    data = request.get_json()
    login, password = data["login"], data["password"]
    if login and password:
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT password, id FROM users WHERE login = %s''',\
            [login])
        (password_hash, user_id) = cursor.fetchone()
        cursor.close()
        if sha256_crypt.verify(password, password_hash):
            session.permanent = True
            session["user_id"] = user_id
            return "ok", 200
        else:
            return "", 401


@app.route("/profile/<user_id>", methods = ['GET', 'POST'])
def profile(user_id):
    if "user_id" in session and session["user_id"] == int(user_id):
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT 
                    name, 
                    surname,
                    age,
                    gender,
                    interests,
                    city
                FROM profiles WHERE user_id = %s''', [user_id])
            profile = cursor.fetchone()
            cursor.close()
            return { "name": profile[0], "surname": profile[1],
                "age": profile[2], "gender": profile[3],
                "interests": profile[4], "city": profile[5] }, 200
        if request.method == 'POST':
            data = request.get_json()
            cursor = mysql.connection.cursor()
            cursor.execute('''INSERT INTO 
                profiles(user_id, name, surname, age, gender, interests, city) 
                VALUES(%s,%s,%s,%s,%s,%s,%s)''',\
                (user_id, data["name"], data["surname"], data["age"],\
                data["gender"], data["interests"], data["city"]))
            mysql.connection.commit()
            cursor.close()
            return "ok", 200
    else:
        return redirect("/login")


@app.route("/friends/<user_id>", methods = ['GET', 'POST'])
def friends(user_id):
    if "user_id" in session and session["user_id"] == int(user_id):
        if request.method == 'GET':
            cursor = mysql.connection.cursor()
            cursor.execute('''
                SELECT 
                    u.login,
                    COALESCE(f1.f1_user_id, f2.f2_user_id)
                FROM users u
                LEFT JOIN friends f1 ON f1.f1_user_id = u.id
                LEFT JOIN friends f2 ON f2.f2_user_id = u.id
                WHERE (f2.f1_user_id = %s AND f2.f1_approved)
                    OR (f1.f2_user_id = %s AND f1.f2_approved)''',\
                    [user_id, user_id])
            friends = cursor.fetchall()
            cursor.close()
            return [{"id": f[1], "login": f[0]} for f in friends], 200
        if request.method == 'POST':
            data = request.get_json()
            cursor = mysql.connection.cursor()
            cursor.execute('''SELECT COUNT(1) FROM friends
                WHERE f1_user_id = %s AND f2_user_id = %s''',\
                    [data["userId"], user_id])
            friend_request = cursor.fetchone()
            if friend_request[0] == 0: # add friends request from user_id
                cursor.execute('''
                    INSERT INTO
                        friends(f1_user_id, f2_user_id, f1_approved, f2_approved) 
                    VALUES(%s,%s,%s,%s)''', (user_id, data["userId"], True, False))
            else: # approve friends request by user_id
                cursor.execute('''
                    UPDATE friends SET f2_approved = true
                    WHERE f1_user_id = %s AND f2_user_id = %s''',\
                        [data["userId"], user_id])
            mysql.connection.commit()
            cursor.close()
            return "ok", 200
    else:
        return redirect("/login")


@app.route("/run_migration")
def run_migration():
    cursor = mysql.connection.cursor()
    with open('init_db.sql', 'r') as f:
        cursor.execute(f.read())
    cursor.close()
    return "Have successfully executed initial migration!"