# Discipliner
#### Video Demo:  <https://youtu.be/ARC2bJx9PUU>
#### Description: The three main parts of my project are described below.
#### Password Manager:
This is a simple password manager to store all your passwords in a sqlite database and with one master password you can look at all your passwords and you don't have to worry about forgeting a password ever again.

To ensure proper safety and prevent your passwords from getting hacked the passwords stored in the database are encrypted using Fernet which provides symmetric encryption. Hence , none of your real passwords are stored on the database rather the encrypted form is stored which is decrypted again when to show you when you request the Password Table/

### Task Manager:
Ever feel like you're loosing track of all the tasks you want to do , Discipliner has a task manager section where you can easily list all your tasks and give them a particular deadline and upon completion of the task you can just tick the checkbox on the right most column. It'll help you get organized and be on track for all your tasks.

Task manager keeps you organized and on track you can create tasks and assign a specific deadline to those tasks , once you're finished doing that task you can simply check the completed box.


### Notes Manager:
How many times have you forgotten important info when you needed it the most , the notes section of Discipliner let's you keep track of all that information by putting it in a table.

The notes manager automatically assigns a date to the content added so that you exactly remember when you added that note and you do not forget the context of the note.
Every note has a title associated with it so that it is easier for you to find notes of specific titles without going through the content of each note.


### Database Explained :
To store data sqlite database was used which consisted of tables :

### Users :
The users table stored the user_id ,username , master password for every user and upon a login request the password provided by the user was checked against the username and password in this table.

To ensure proper security measures the master password is stored in an encrypted manner using the encryption provided by werkzeug.security

#### Technologies Used :
 * Python
 * Flask
 * HTML
 * CSS
 * Bootstrap
 * Fernet


#### How to Run:
* Download the Source Code
* Locate app.Py
* Run pip install requirements.txt
* Run flask run
* (Optional) Run phpliteadmin database.db to check the database and see the tables


#### Documentation :
 * Flask - <https://flask.palletspro jects.com/en/2.2.x/>
 * Python - <https://docs.python.org/3/>
 * Sqlite3 - <https://www.sqlite.org/docs.html>
 * Fernet - <https://cryptography.io/en/latest/fernet/>
 * Bootstrap - <https://getbootstrap.com/docs/5.0/getting-started/introduction/>




#### About CS50:
CS50 is a openware course from Havard University and taught by David J. Malan

Introduction to the intellectual enterprises of computer science and the art of programming. This course teaches students how to think algorithmically and solve problems efficiently. Topics include abstraction, algorithms, data structures, encapsulation, resource management, security, and software engineering. Languages include C, Python, and SQL plus students’ choice of: HTML, CSS, and JavaScript (for web development).

Thank you for all CS50.

