import MySQLdb
import json

def db_query(query, args):
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  # your password
                     db="NotesApp")        # name of the data base
    cur = db.cursor()
    cur.execute(query, args)
    db.commit()
    db.close()
    return cur

def db_query_return_id(query, args):
    db = MySQLdb.connect(host="localhost", user="root", passwd="", db="NotesApp")
    cur = db.cursor()
    cur.execute(query, args)
    db.commit()
    cur.execute("SELECT LAST_INSERT_ID();")
    insertedID =  int(cur.fetchone()[0])
    db.close()
    return insertedID
