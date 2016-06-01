import MySQLdb
import json

def db_query(query, args):
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  # your password
                     db="NotesApp")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
    cur = db.cursor()

# Use all the SQL you like
    cur.execute(query, args)
    db.commit()
# print all the first cell of all the rows
#for row in cur.fetchall():
#    print row[0]

    db.close()

    json_string = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
    #json_string = json.dumps(dict(cur.fetchall()))
    #json_string = json.dumps(cur.fetchall())
    return json.dumps(json_string)
    #return cur.fetchall()
