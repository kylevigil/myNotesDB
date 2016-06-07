from dbConnector import *
import bcrypt
import re

def checkUsername(username):
    query = "SELECT COUNT(*) FROM Users WHERE username = %s"
    args = [username]
    tempResult = db_query(query, args).fetchall()
    result = int(tempResult[0][0])
    if result >= 1:
        return True
    return False

def checkUser(username, passHash):
    if checkUsername(username):
        query = "SELECT COUNT(*) FROM Users WHERE username = %s \
            AND passHash = %s;"
        salt = db_query("SELECT salt FROM Users WHERE username = %s;", username)
        salt = salt.fetchall()
        newPassHash = bcrypt.hashpw(passHash, salt[0][0])
        args = [username, newPassHash]
        tempResult = db_query(query, args).fetchall()
        result = int(tempResult[0][0])
        if result >= 1:
            return True
    return False

def addUser(postvars):
    query = "INSERT INTO Users(username, salt, passHash) \
            VALUES (%s, %s, %s);"
    salt = bcrypt.gensalt()
    newPassHash = bcrypt.hashpw(postvars['passHash'][0], salt)
    args = [postvars['username'][0], salt, newPassHash]
    return db_query(query, args)

def addNote(postvars):
    query = "INSERT INTO Notes(user, noteText, lastModified, title) \
            VALUES (%s, %s, NOW(), %s);"
    args = [postvars['username'][0], postvars['noteText'][0], postvars['title'][0]]

    noteID = db_query_return_id(query, args)
    parseTags(postvars['noteText'][0], noteID)
   
def modifyNote(postvars):
    query = "UPDATE Notes SET noteText = %s, title = %s, lastModified = NOW() \
            WHERE id = %s;"
    args = [postvars['noteText'][0], postvars['title'][0], postvars['id'][0]]
    db_query(query, args)

    noteID = postvars['id'][0]
    #Need to delete previous tags for this note
    db_query("DELETE FROM NoteTags WHERE note = %s", [noteID])

    parseTags(postvars['noteText'][0], postvars['id'][0])
    return db_query(query, args)
    

def deleteNote(postvars):
    query = "DELETE FROM NoteTags WHERE note = %s;"
    args = [postvars['id'][0]]
    db_query(query, args)
    query = "DELETE FROM Notes WHERE id = %s;"
    db_query(query, args)
    

def getNotes(postvars):
    query = "SELECT N.id, title, GROUP_CONCAT(T.tag SEPARATOR ' ') AS tags FROM Notes N\
            LEFT JOIN NoteTags NT ON NT.note = N.id \
            LEFT JOIN Tags T ON T.id = NT.tag \
            WHERE user = %s GROUP BY N.id, title \
            ORDER BY lastModified DESC;"
    args = [postvars['username'][0]]
    return db_query(query, args)

def getNote(postvars):
    query = "SELECT id, title, noteText FROM Notes \
            WHERE id = %s;"
    args = [postvars['id'][0]]
    return db_query(query, args)

def search(postvars):
    query = "SELECT N.id, title, GROUP_CONCAT(T.tag SEPARATOR ' ') AS tags FROM Notes N\
            LEFT JOIN NoteTags NT ON NT.note = N.id \
            LEFT JOIN Tags T ON T.id = NT.tag \
            WHERE user = %s \
            AND (LOWER(title) LIKE LOWER(%s) \
            OR LOWER(noteText) LIKE LOWER(%s)) \
            GROUP BY N.id, title \
            ORDER BY lastModified DESC;"
    likeString = '%' + postvars['string'][0] + '%'
    args = [postvars['username'][0], likeString, likeString]
    return db_query(query, args)
    

#WHERE title LIKE or tag like %search%


def parseTags(noteText, id):
    wordList = set(part[1:] for part in noteText.split() if part.startswith('#'))
    wordList = set(re.split(r'\W+', i)[0] for i in wordList)
    insert_query = "INSERT INTO Tags(tag) VALUES (%s);"
    check_query = "SELECT id FROM Tags WHERE tag = %s"
    for word in wordList:
        if word == ' ' or word == '' or word is None:
            continue
        queryResult = db_query(check_query, [word])
        tagID = None
        if queryResult.rowcount >= 1:
            tagID = int(queryResult.fetchone()[0])

        #Insert tag into database
        args = [word]
        if tagID is None:
            tagID = db_query_return_id(insert_query, args)

        args = [id, tagID]
        #Update the NoteTags table
        db_query("INSERT INTO NoteTags(note, tag) VALUES (%s, %s)", args)

