from dbConnector import *
import bcrypt

def checkUsername(username):
    query = "SELECT COUNT(*) FROM Users WHERE username = %s"
    args = [username]
    tempResult = db_query(query, args).fetchall()
    #print "!!!" + tempResult
    result = int(tempResult[0][0])
    print result
    print "result"
    if result >= 1:
        return True
    return False

def checkUser(username, passHash):
    if checkUsername(username):
        query = "SELECT COUNT(*) FROM Users WHERE username = %s \
            AND passHash = %s;"
        salt = db_query("SELECT salt FROM Users WHERE username = %s;", username)
        #print salt[0][0]
        salt = salt.fetchall()
        newPassHash = bcrypt.hashpw(passHash, salt[0][0])
        print "hi " + newPassHash
        args = [username, newPassHash]
        tempResult = db_query(query, args).fetchall()
       # print "***" + db_query(query, args)
        result = int(tempResult[0][0])
        if result >= 1:
            return True
    return False

def addUser(postvars):
    query = "INSERT INTO Users(username, salt, passHash) \
            VALUES (%s, %s, %s);"
    salt = bcrypt.gensalt()
    print "salt: " + salt
    newPassHash = bcrypt.hashpw(postvars['passHash'][0], salt)
    print "newPassHash: " + newPassHash
    args = [postvars['username'][0], salt, newPassHash]
    return db_query(query, args)

def addNote(postvars):
    query = "INSERT INTO Notes(user, noteText, lastModified, title) \
            VALUES (%s, %s, NOW(), %s);"
    args = [postvars['username'][0], postvars['noteText'][0], postvars['title'][0]]

    #cur = db_query(query, args)
    #print db_query("SELECT LAST_INSERT_ID();", []).fetchall()
    #noteID = int(db_query("SELECT LAST_INSERT_ID();", []).fetchall()[0][0])
    noteID = db_query_return_id(query, args)
    parseTags(postvars['noteText'][0], noteID)
    #return cur
   
def modifyNote(postvars):
    query = "UPDATE Notes SET noteText = %s, title = %s, lastModified = NOW() \
            WHERE id = %s;"
    args = [postvars['noteText'][0], postvars['title'][0], postvars['id'][0]]
    db_query(query, args)

    noteID = postvars['id'][0]
    #Need to delete previous tags for this note
    db_query("DELETE FROM NoteTags WHERE note = %s", [noteID])
    #db_query("DELETE FROM Tags WHERE note = %s", [noteID])

    parseTags(postvars['noteText'][0], postvars['id'][0])
    return db_query(query, args)
    

def deleteNote(postvars):
    query = "DELETE FROM NoteTags WHERE note = %s;"
    args = [postvars['id'][0]]
    db_query(query, args)
    query = "DELETE FROM Notes WHERE id = %s;"
    db_query(query, args)
    

def getNotes(postvars):
    query = "SELECT N.id, title, T.tag FROM Notes N\
            JOIN NoteTags NT ON NT.note = N.id \
            JOIN Tags T ON T.id = NT.tag \
            WHERE user = %s ORDER BY lastModified DESC;"
    args = [postvars['username'][0]]
    return db_query(query, args)

def getNote(postvars):
    query = "SELECT id, title, noteText FROM Notes \
            WHERE id = %s;"
    args = [postvars['id'][0]]
    return db_query(query, args)

def search(postvars):
    query = "SELECT id, title FROM Notes \
            WHERE title LIKE %s \
            OR noteText LIKE '%%s%' \
            ;"
    args = [postvars['string'][0]]
    return db_query(query, args)
    

#WHERE title LIKE or tag like %search%


def parseTags(noteText, id):
    wordList = set(part[1:] for part in noteText.split() if part.startswith('#'))
    query = "INSERT INTO Tags(tag) VALUES (%s);"
    for word in wordList:
        #Insert tag into database
        args = [word]
        tagID = db_query_return_id(query, args)

        args = [id, tagID]
        print "id: " + str(id)
        print "tagID: " + str(tagID)
        #Update the NoteTags table
        db_query("INSERT INTO NoteTags(note, tag) VALUES (%s, %s)", args)
        print "Tag: " + word

