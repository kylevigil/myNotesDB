from dbConnector import *

def addUser(postvars):
    query = "INSERT INTO Users(username, salt, passHash) \
            VALUES (%s, %s, %s);"
    args = [postvars['username'][0], postvars['salt'][0], postvars['passhash'][0]]
    return db_query(query, args)

def addNote(postvars):
    query = "INSERT INTO Notes(user, noteText, lastModified, title) \
            VALUES (%s, %s, NOW(), %s);"
    args = [postvars['user'][0], postvars['noteText'][0], postvars['title'][0]]
    return db_query(query, args)
   
def modifyNote(postvars):
    query = "UPDATE Notes SET noteText = %s, title = %s, lastModified = NOW() \
            WHERE id = %s;"
    args = [postvars['noteText'][0], postvars['title'][0], postvars['id'][0]]
    return db_query(query, args)
    

def deleteNote(postvars):
    query = "DELETE FROM Notes WHERE id = %s;"
    args = [postvars['id'][0]]
    return db_query(query, args)

def getNotes(postvars):
    query = "SELECT id, title FROM Notes \
            WHERE user = %s ORDER BY lastModified DESC;"
    args = [postvars['user'][0]]
    return db_query(query, args)
    
