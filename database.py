import psycopg2

# def create():
#     db_connection = psycopg2.connect("dbname='database' user='postgres' password='1Lomkones.' host='localhost'")
#     db_cursor = db_connection.cursor()
#     db_cursor.execute("CREATE TABLE IF NOT EXISTS store (item TEXT, quantity INTEGER, price REAL)") # REAL is a float
#     db_connection.commit()
#     db_connection.close()

# def insert(item, quantity, price):
#     db_connection = psycopg2.connect("dbname='database' user='postgres' password='1Lomkones.' host='localhost'")
#     db_cursor = db_connection.cursor()
#     db_cursor.execute("INSERT INTO store VALUES (%s,%s,%s)", (item, quantity, price))
#     db_connection.commit()
#     db_connection.close()

def view(email):
    # db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
    # db_cursor = db_connection.cursor()
    # db_cursor.execute("SELECT users.email FROM users WHERE user_id=%s", (user_id,))
    # rows = db_cursor.fetchall()
    # print(rows)
    db_connection = psycopg2.connect("dbname='local_db_1' user='postgres' password='1Lomkones.' host='localhost'")
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT * FROM users WHERE username=%s", (email,))
    row = db_cursor.fetchall()
    for each in row:
        print(each[4])



view("driver@gmail.com")
# insert("Tablet", 2, 140999)
# insert("Toshiba", 10, 30000)
# insert("Infinix", 3, 12000)
# print(view())
# delete("Toshiba")
# update("Macbook", 14, 199990.9)
# print(view())