from faker import Faker
from pymysql import connect


connection = connect(host='localhost',
                    port=3301,
                    user='flask',
                    password='ksalf',
                    db='social_network')

# run initial migration
with connection.cursor() as cursor:
    with open('init_db.sql', 'r') as f:
        cursor.execute(f.read())
    
    connection.commit()

    print("Have successfully executed initial migration!")

    # add test data
    # fake = Faker()
    # for i in range(100):
    #     for j in range(100):
    #         cursor.execute('''INSERT INTO 
    #         profiles(firstName, secondName, interests, city) 
    #         VALUES(%s,%s,%s,%s)''',\
    #         (fake.first_name(), fake.last_name(), fake.text(), fake.city()))
    #     connection.commit()
    #     print("Have committed "+str((i+1)*100)+" profiles")

connection.close()

print("Success!")