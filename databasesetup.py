import psycopg2
import sys
import models

def drop():
    try:
        db_connection = psycopg2.connect(models.db)
        db_cursor = db_connection.cursor()
        db_cursor.execute('DROP TABLE IF EXISTS "users", "rides","request";')
        db_connection.commit()
        db_connection.close()
    except psycopg2.Error:
        raise SystemExit("Failed {}".format(sys.exc_info()))
       
def tables_creation():
    try:
        tables = ("""CREATE TABLE IF NOT EXISTS users (user_id SERIAL PRIMARY KEY, email VARCHAR(150) NOT NULL UNIQUE,
                                                    username VARCHAR(100) NOT NULL, password VARCHAR(450) NOT NULL,
                                                    admin BOOLEAN NOT NULL)""",
                """ CREATE TABLE IF NOT EXISTS rides (ride_id SERIAL PRIMARY KEY, ride VARCHAR(155) NOT NULL,
                                                        driver_id VARCHAR(50) NOT NULL, departuretime VARCHAR(100) NOT NULL,
                                                        numberplate VARCHAR(100) NOT NULL, maximum VARCHAR(100) NOT NULL,
                                                        status VARCHAR(100) NOT NULL)""",
                """ CREATE TABLE IF NOT EXISTS request (request_id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL,
                                                        ride_id INTEGER NOT NULL, status VARCHAR(100) NOT NULL,
                                                        accepted BOOLEAN NOT NULL)""")
        conn = psycopg2.connect(models.db)
        cur = conn.cursor()
        for table in tables:
            cur.execute(table)
        cur.close()
        conn.commit()

    except psycopg2.Error:
        raise SystemExit("Failed {}".format(sys.exc_info()))
 

drop()
tables_creation()

print ("--------- CREATED TABLES ---------")