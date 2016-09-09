# coding:utf-8

# Connect to the database
import mysql.connector
from mysql.connector import errorcode
import settings
from datetime import date, datetime, timedelta

# mysql connection
try:
    cnx = mysql.connector.connect(
        host=settings.dbhost,
        user=settings.dbuser,
        password=settings.dbpassword,
        db=settings.dbname,
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

cur = cnx.cursor()


# show all tables in the database
def showtables(cursor):
    # show tables in DB
    query = "SHOW TABLES from " + settings.dbname + ";"
    print(query)
    #cursor.execute(query)
    cursor.execute("SHOW TABLES;")
    result = cursor.fetchall()
    print(result)

# create tables in the database
def createtables(cursor):
    TABLES = {}

    TABLES['daily_pos'] = (
        "CREATE TABLE `daily_pos` ("
        "  `isbn` char(13) NOT NULL,"
        "  `pos` int(3) NOT NULL,"
        "  `date` date NOT NULL"
        ") ENGINE=InnoDB")

    # In python3, we shoule use 'items' instead of 'iteritems' in python2.
    for name, ddl in TABLES.items():
        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")


def insertdata(cursor):
    add_pos = ("INSERT INTO daily_pos "
                    "(isbn, pos, date) "
                    "VALUES (%s, %s, %s)")

    data_pos = ('0000000000000', '0', date(2016, 9, 9))

    cursor.execute(add_pos, data_pos)
    cnx.commit()

if __name__ == '__main__':
    print('Hello!')
    showtables(cur)
    insertdata(cur)

    # close the sql connection
    cur.close()
    cnx.close()
