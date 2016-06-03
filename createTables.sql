DROP TABLE IF EXISTS NoteTags;
DROP TABLE IF EXISTS Notes;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
   username VARCHAR(32) NOT NULL,
   salt CHAR(29),
   passHash CHAR(60),
   PRIMARY KEY(username)
);

CREATE TABLE Tags (
   id INT NOT NULL AUTO_INCREMENT,
   tag VARCHAR(64),
   PRIMARY KEY(id)
);

CREATE TABLE Notes (
   id INT NOT NULL AUTO_INCREMENT,
   user VARCHAR(32),
   noteText BLOB,
   lastModified TIMESTAMP,
   title VARCHAR(64),
   PRIMARY KEY(id),
   FOREIGN KEY (user) REFERENCES Users(username)
);

CREATE TABLE NoteTags (
   note INT,
   tag INT,
   FOREIGN KEY(note) REFERENCES Notes(id),
   FOREIGN KEY(tag) REFERENCES Tags(id)
);

-- INSERT INTO Users(username, salt, passHash)
-- VALUES 
--   ('george', 'ABC123', 'h32ouih32uhs3h1b123456789012345u'),
--   ('jake', 'ABC123', 'h32ouih32uhs3h1b123456789012345u'),
--   ('kyle', 'ABC123', 'h32ouih32uhs3h1b123456789012345u'),
--   ('eriq', 'ABC123', 'h32ouih32uhs3h1b123456789012345u')
-- ;
