DROP TABLE IF EXISTS NoteTags;
DROP TABLE IF EXISTS Notes;
DROP TABLE IF EXISTS Tags;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
   id INT NOT NULL AUTO_INCREMENT,
   username VARCHAR(32),
   salt CHAR(6),
   passHash CHAR(32),
   PRIMARY KEY(id)
);

CREATE TABLE Tags (
   id INT NOT NULL AUTO_INCREMENT,
   tag VARCHAR(64),
   PRIMARY KEY(id)
);

CREATE TABLE Notes (
   id INT NOT NULL AUTO_INCREMENT,
   user INT,
   noteText BLOB,
   lastModified TIMESTAMP,
   title VARCHAR(64),
   PRIMARY KEY(id),
   FOREIGN KEY (user) REFERENCES Users(id)
);

CREATE TABLE NoteTags (
   note INT,
   tag INT,
   FOREIGN KEY(note) REFERENCES Notes(id),
   FOREIGN KEY(tag) REFERENCES Tags(id)
);

INSERT INTO Users(username, salt, passHash)
 VALUES 
   ('george', 'ABC123', 'h32ouih32uhs3h1b123456789012345u'),
   ('jake', 'ABC123', 'h32ouih32uhs3h1b123456789012345u'),
   ('kyle', 'ABC123', 'h32ouih32uhs3h1b123456789012345u'),
   ('eriq', 'ABC123', 'h32ouih32uhs3h1b123456789012345u')
;
