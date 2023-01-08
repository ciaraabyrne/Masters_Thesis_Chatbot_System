import mysql.connector
import pymysql.cursors
import re


def DataUpdate(name, Email, dispatcher):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")
    mycursor = mydb.cursor()
    sql = "INSERT INTO rasa_person (name, Email) VALUES (%s, %s)"
    vals = (name, Email)
    mycursor.execute(sql, vals)
    mydb.commit()
    dispatcher.utter_message(f" {name} was commited to database")


def dataQuery(person_id, dispatcher):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")

    mycursor = mydb.cursor()
    sql = 'SELECT name from rasa_person where id="{0}";'.format(person_id)

    try:
        # Execute the SQL Query
        mycursor.execute(sql)
        results = mycursor.fetchall()
        for row in results:
            name = row[0]
            # Now print gethced data
            # dispatcher.utter_message(f"User Name: {name}")
            dispatcher.utter_message(response="utter_response", name=name)
    except:
        dispatcher.utter_message("Error : Unable to fetch data.")


def dataGetId(name, Email, dispatcher):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")

    mycursor = mydb.cursor()
    sql = "SELECT id FROM rasa_person WHERE name='%s' AND Email='%s'" % (name, Email)

    try:
        # Execute the SQL Query
        mycursor.execute(sql)
        results = mycursor.fetchall()
        for row in results:
            id = row[0]
            # Now print gethced data
            dispatcher.utter_message(f"Your ID is {id}, remember this so we can pick up where we left off next time!")

    except:
        dispatcher.utter_message("Error : Unable to fetch data.")


def dataGetPrevQ(id, dispatcher):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")

    mycursor = mydb.cursor()
    sql = 'SELECT level_sql FROM rasa_person WHERE id="{0}";'.format(id)

    try:
        # Execute the SQL Query
        mycursor.execute(sql)
        results = mycursor.fetchall()

        for row in results:
            level_sql = row[0]
            # dispatcher.utter_message(
            #     f"your level_sql is \n {level_sql} \n ")
            sql2 = "SELECT q_name FROM SQL_level WHERE level='%s'" % (level_sql)

            mycursor.execute(sql2)
            results2 = mycursor.fetchall()

            #   for rows in results2:
            q_name = results2[0]

            # Now print gethced data
            # dispatcher.utter_message(response="utter_lastquestion", exercise=level_sql)
            # dispatcher.utter_message(f"Last time we tried a question like \n {q_name} \n Do you want to try a similar question or move on?")
            return q_name, level_sql

    except:
        dispatcher.utter_message("Error : Unable to fetch data.")


def dataGetNewQ(name, id, dispatcher, level_sql, exercise_id):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")

    mycursor = mydb.cursor()
    sql = 'SELECT level_sql FROM rasa_person WHERE id="{0}";'.format(id)
    # check if they want same or next level

    if name == 'similar':
        sql2 = "SELECT question,Question_id FROM SQL_level WHERE level='%s' AND Question_id !='%s'" % (
            level_sql, exercise_id)
        try:
            # Execute the SQL Query
            mycursor.execute(sql2)
            results = mycursor.fetchall()

            for row in results:
                # dispatcher.utter_message(f"resuls[0] \n {row[0]} \n ")
                # dispatcher.utter_message(f"resuls[0] \n {row[1]} \n ")
                question = row[0]
                q_id = row[1]
                # dispatcher.utter_message( f"your level_sql is \n {level_sql} \n ")

                return question, q_id, level_sql
        except:
            dispatcher.utter_message("Error : Unable to fetch data.")

    if name == 'move_on':
        level_sql = level_sql + 1
        sql2 = "SELECT question,Question_id FROM SQL_level WHERE level='%s'" % (level_sql)
        try:
            # Execute the SQL Query
            mycursor.execute(sql2)
            results = mycursor.fetchall()
            for row in results:
                # dispatcher.utter_message(f"resuls[0] \n {row[0]} \n ")
                # dispatcher.utter_message(f"resuls[0] \n {row[1]} \n ")
                question = row[0]
                q_id = row[1]
                # dispatcher.utter_message(f"your level_sql is \n {level_sql} \n ")

                return question, q_id, level_sql

        except:
            dispatcher.utter_message("Error : Unable to fetch data.")


def dataCheckAnswer(answer, exercise_id, dispatcher, id):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")

    mycursor = mydb.cursor()
    # mycursor_name = mydb.cursor()
    sql = "SELECT answer FROM SQL_level WHERE Question_id='%s'" % (exercise_id)
    sql_name = 'SELECT name from rasa_person where id="{0}";'.format(id)
    # check if they want same or next level

    try:
        # Execute the SQL Query
        mycursor.execute(sql)
        results = mycursor.fetchall()

        for row in results:
            ans = row[0]
            #   name1 = row[1]
            # dispatcher.utter_message(f"ans: {ans}")
            # dispatcher.utter_message(f"answer: {answer}")
            # dispatcher.utter_message(f"name1: {name1}")

            if answer == ans:
                # reply = "Correct! Well done " + name1
                dispatcher.utter_message(f"Correct! Well done")
                reply2 = "Correct"
                return reply2

            else:
                # reply = "Hard luck " + name1 + ". Try again!"
                dispatcher.utter_message(f"Hard luck. Try again!")
                reply2 = "Incorrect"
                return reply2


    except:
        dispatcher.utter_message("Error : Unable to fetch data.")


def dataUpdateOnQuit(id, level, dispatcher):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")
    mycursor = mydb.cursor()
    sql = "UPDATE rasa_person SET level_sql='%s' WHERE id='%s'" % (level, id)
    mycursor.execute(sql)
    mydb.commit()
    dispatcher.utter_message(f" Bye {id}! I hope to see you again soon")


def dataGeneralQuestion(message, level, dispatcher):
    msg = message.lower()
    if 'syntax' in msg:
        if level == 1:
            dispatcher.utter_message(
                f" Remember you learned about the SELECT statement? \n Try this syntax in your exercise: \n SELECT column1, column2  \n FROM table_name;")
        if level == 2:
            dispatcher.utter_message(
                f" Remember you learned about the SELECT statement? \n Try this syntax in your exercise: \n SELECT * FROM table_name;")
        if level == 3:
            dispatcher.utter_message(
                f" Remember you learned about the SELECT DISTINCT statement? \n Try this syntax in your exercise: \n SELECT DISTINCT column1, column2 \n FROM table_name;")

    if 'theory' in msg:
        if level == 1:
            dispatcher.utter_message(
                f" Remember you learned about the SELECT statement?  \n SELECT - extracts data from a database.")
        if level == 2:
            dispatcher.utter_message(
                f" Remember you learned about the SELECT * statement?  \n SELECT * - returns all values in a table.")
        if level == 3:
            dispatcher.utter_message(
                f" Remember you learned about the SELECT DISTINCT statement? \n The SELECT DISTINCT statement is used to return only distinct (different) values. \n Inside a table, a column often contains many duplicate values and sometimes you only want to list the different (distinct) values.")

