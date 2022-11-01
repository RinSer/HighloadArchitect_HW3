from flask import Flask, request
from pymysql import connect
from faker import Faker


app = Flask(__name__)

def mysql():
    return connect(host='localhost',
                    port=3301,
                    user='flask',
                    password='ksalf',
                    db='social_network')

def mysql2():
    return connect(host='localhost',
                    port=3302,
                    user='flask',
                    password='ksalf',
                    db='social_network')

def mysql3():
    return connect(host='localhost',
                    port=3302,
                    user='flask',
                    password='ksalf',
                    db='social_network')

fake = Faker()


@app.route("/profiles", methods = ['GET', 'POST'])
def profiles():
    if request.method == 'GET':
        conn = mysql2()
        cursor = conn.cursor()
        cursor.execute('''SELECT 
                id,
                firstName, 
                secondName,
                interests,
                city
            FROM profiles''')
        profiles = cursor.fetchall()
        cursor.close()
        conn.close()
        return [{ 
            "id": profile[0],
            "firstName": profile[1], 
            "secondName": profile[2],
            "interests": profile[3],
            "city": profile[4] } for profile in profiles], 200
    if request.method == 'POST':
        conn = mysql()
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO 
            profiles(firstName, secondName, interests, city) 
            VALUES(%s,%s,%s,%s)''',\
            (fake.first_name(), fake.last_name(), fake.text(), fake.city()))
        mysql.commit()
        cursor.close()
        conn.close()
        return "ok", 200
        
        
@app.route("/profile/<id>", methods = ['GET', 'PUT'])
def profile(id):
    if request.method == 'GET':
        conn = mysql2()
        cursor = conn.cursor()
        cursor.execute('''SELECT 
                id,
                firstName, 
                secondName,
                interests,
                city
            FROM profiles WHERE id = %s''', [id])
        profile = cursor.fetchone()
        cursor.close()
        conn.close()
        return { 
            "id": profile[0],
            "firstName": profile[1], 
            "secondName": profile[2],
            "interests": profile[3],
            "city": profile[4] }, 200
    if request.method == 'PUT':
        data = request.get_json()
        conn = mysql()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE profiles SET
                firstName = %s, 
                secondName = %s, 
                interests = %s, 
                city = %s 
            WHERE id = %s''',\
            [data["firstName"], data["secondName"], 
            data["interests"], data["city"], id])
        mysql.commit()
        cursor.close()
        conn.close()
        return "ok", 200