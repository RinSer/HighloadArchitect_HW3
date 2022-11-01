from flask import Flask, request
from flask_mysqldb import MySQL
from faker import Faker


app = Flask(__name__)

app.secret_key = 'some_secret'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3301
app.config['MYSQL_USER'] = 'flask'
app.config['MYSQL_PASSWORD'] = 'ksalf'
app.config['MYSQL_DB'] = 'social_network'
 
mysql = MySQL(app)

fake = Faker()


@app.route("/profiles", methods = ['GET', 'POST'])
def profiles():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT 
                id,
                firstName, 
                secondName,
                interests,
                city
            FROM profiles''')
        profiles = cursor.fetchall()
        cursor.close()
        return [{ 
            "id": profile[0],
            "firstName": profile[1], 
            "secondName": profile[2],
            "interests": profile[3],
            "city": profile[4] } for profile in profiles], 200
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO 
            profiles(firstName, secondName, interests, city) 
            VALUES(%s,%s,%s,%s)''',\
            (fake.first_name(), fake.last_name(), fake.text(), fake.city()))
        mysql.connection.commit()
        cursor.close()
        return "ok", 200
        
        
@app.route("/profile/<id>", methods = ['GET', 'PUT'])
def profile(id):
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        cursor.execute('''SELECT 
                id,
                firstName, 
                secondName,
                interests,
                city
            FROM profiles WHERE id = %s''', [id])
        profile = cursor.fetchone()
        cursor.close()
        return { 
            "id": profile[0],
            "firstName": profile[1], 
            "secondName": profile[2],
            "interests": profile[3],
            "city": profile[4] }, 200
    if request.method == 'PUT':
        data = request.get_json()
        cursor = mysql.connection.cursor()
        cursor.execute('''
            UPDATE profiles SET
                firstName = %s, 
                secondName = %s, 
                interests = %s, 
                city = %s 
            WHERE id = %s''',\
            [data["firstName"], data["secondName"], 
            data["interests"], data["city"], id])
        mysql.connection.commit()
        cursor.close()
        return "ok", 200