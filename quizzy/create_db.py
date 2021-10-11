
import sqlite3
import sys
import datetime
try:
    db_conn = sqlite3.connect('quizzy.db');        # Get database connection object
    cursor = db_conn.cursor();                     # Get a cursor object for the connection
    print ("Opened database");
except Exception as e:
    print("Error connection to the DB: " + str(e)); # Print error message
    sys.exit()
## -------------------------------------
## Create table and close connection
# Print error messag

try:
    sql = 'DROP TABLE IF EXISTS category_question'; # Open the database

    cursor.execute(sql);

    sql = '''CREATE TABLE category_question(
                cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT not null,
                sub_category TEXT not null);''';

    cursor.execute(sql); # Create product table with constraints
    print ("Table category_question created");
    db_conn.commit();
except Exception as e:
    print("Error creating tables: " + str(e));    # Print error message

try:
    sql = """
    INSERT INTO category_question (category, sub_category) values ('python', 'data type');
    INSERT INTO category_question (category, sub_category) values ('python', 'loop');
    INSERT INTO category_question (category, sub_category) values ('sql', 'cursors');
    INSERT INTO category_question (category, sub_category) values ('sql', 'relationship');
    INSERT INTO category_question (category, sub_category) values ('English', 'vocabulary');
    INSERT INTO category_question (category, sub_category) values ('English', 'granma');

    """
    cursor.executescript(sql);
    db_conn.commit();

    _sql = """ SELECT * from category_question """;
    cursor.execute(_sql);
    for row in cursor.fetchall():
        print(row);

except Exception as e:
    print("Error insearting tables: " + str(e));    # Print error message

##########################################################################
###Create question tables

try:
    sql = 'DROP TABLE IF EXISTS question'; # Open the database
    cursor.execute(sql);
    sql = '''CREATE TABLE question(
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT not null,
                correct_choice TEXT not null,
                choice1 TEXT not null,
                choice2 TEXT not null,
                choice3 TEXT not null,
                cat_id INTEGER not null, FOREIGN KEY(cat_id) REFERENCES category_question(cat_id) ON DELETE CASCADE
                );''';

    cursor.executescript(sql); # Create product table with constraints
    print ("Table question created");
    db_conn.commit();
except Exception as e:
    print("Error creating tables: " + str(e));    # Print error message

try:
    sql = """
    INSERT INTO question (question, cat_id, correct_choice, choice1, choice2, choice3)
     values ('Which of these is not a core data type?', 1, 'Class', 'List', 'Dictionary','Tuple');
    INSERT INTO question (question, cat_id, correct_choice, choice1, choice2, choice3)
    values ('Click the best synonym for diet:', 5, 'Food', 'Smile', 'Exercise','Yard');
    INSERT INTO question (question, cat_id, correct_choice, choice1, choice2, choice3)
   values ('Click the best synonym for rip:', 5, 'Tear', 'Enhance', 'Smash','Abolish');
    INSERT INTO question (question, cat_id, correct_choice, choice1, choice2, choice3)
    values ('Click the best synonym for gregarious:', 5, 'Outgoing', 'Pushy', 'Graceful','Withdrawn');
    INSERT INTO question (question, cat_id, correct_choice, choice1, choice2, choice3)
    values ('Click the best synonym for matter:', 5, 'Issue', 'Motion', 'Movement','Proof');
    """
    cursor.executescript(sql);
    db_conn.commit();

    _sql = """ SELECT * from question """;
    cursor.execute(_sql);
    for row in cursor.fetchall():
        print(row);

except Exception as e:
    print("Error insearting tables: " + str(e));    # Print error message
    sys.exit()


##########################################################################
###Create question tables

try:
    sql = 'DROP TABLE IF EXISTS user'; # Open the database
    cursor.execute(sql);
    sql = '''CREATE TABLE user(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT not null,
                category TEXT not null,
                create_date TEXT not null,
                correct_answers INTEGER not null,
                browser TEXT not null
                );''';
    cursor.executescript(sql); # Create product table with constraints
    print ("Table user created");
    db_conn.commit();
except Exception as e:
    print("Error creating tables: " + str(e));    # Print error message

except Exception as e:
    print("Error insearting tables: " + str(e));    # Print error message


##########################################################################
###Create user_question_answer tables

try:
    sql = 'DROP TABLE IF EXISTS user_question_answer'; # Open the database
    cursor.execute(sql);
    sql = '''CREATE TABLE user_question_answer(
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER not null,
                question_id INTEGER not null,
                is_correct INTEGER not null,
                FOREIGN KEY(question_id) REFERENCES question(question_id) ON DELETE CASCADE,
                FOREIGN KEY(user_id) REFERENCES user(user_id) ON DELETE CASCADE
                );''';

    cursor.executescript(sql); # Create product table with constraints
    print ("Table user_question_answer created");
    db_conn.commit();
except Exception as e:
    print("Error creating tables: " + str(e));    # Print error message

try:
    sql = """
    INSERT INTO user_question_answer (user_id, question_id, is_correct)
     values (1, 2, 1);
    """
    cursor.execute(sql);
    db_conn.commit();

    _sql = """ SELECT * from user_question_answer """;
    cursor.execute(_sql);
    for row in cursor.fetchall():
        print(row);

except Exception as e:
    print("Error insearting tables: " + str(e));    # Print error message

cursor.close();        # Close the database connection
db_conn.close();
print ("Closed database");
sys.exit()
