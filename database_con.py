import mysql.connector
import pymysql.cursors
import re
from mysql.connector import errorcode


def DataUpdate(name, Email, dispatcher):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")
    mycursor = mydb.cursor()
    sql = "INSERT INTO rasa_person (name, Email) VALUES (%s, %s)"
    vals = (name, Email)
    mycursor.execute(sql, vals)
    mydb.commit()
    # dispatcher.utter_message(f" {name} was commited to database")


def dataQuery(person_id, dispatcher):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")

    mycursor = mydb.cursor()
    sql = "SELECT name from rasa_person where id='%s'" % (person_id)

    try:
        # Execute the SQL Query
        mycursor.execute(sql)
        results = mycursor.fetchall()
        for row in results:
            name = row[0]
            # Now print gethced data
            # dispatcher.utter_message(f"User Name: {name}")
            # dispatcher.utter_message(response="utter_response", name=name)
            return name
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
            return id

    except:
        dispatcher.utter_message("Error : Unable to fetch data.")


def dataGetPrevQ(id, dispatcher):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")

    mycursor = mydb.cursor()
    sql = "SELECT level_sql,last_question_score,name FROM rasa_person WHERE id='%s'" % (id)

    try:
        # Execute the SQL Query
        mycursor.execute(sql)
        results = mycursor.fetchall()

        for row in results:
            level_sql = row[0]
            last_question_score = row[1]
            name = row[2]
            # dispatcher.utter_message(
            #     f"your level_sql is \n {level_sql} \n ")
            sql2 = "SELECT q_name,Question_id FROM SQL_level WHERE level='%s'" % (level_sql)

            mycursor.execute(sql2)
            results2 = mycursor.fetchall()

            for rows in results2:
                q_name = rows[0]
                qid = rows[1]

                # Now print gethced data
                # dispatcher.utter_message(response="utter_lastquestion", exercise=level_sql)
                # dispatcher.utter_message(f"Last time we tried a question like \n {q_name} \n Do you want to try a similar question or move on?")
                return q_name, level_sql, last_question_score, name, qid

    except:
        dispatcher.utter_message("Error : Unable to fetch data.")


def dataGetNewQ(name, id, dispatcher, level_sql, exercise_id, n_correct_qs):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")

    mycursor = mydb.cursor()
    sql = 'SELECT level_sql FROM rasa_person WHERE id="{0}";'.format(id)
    # check if they want same or next level

    if name == 'similar':
        # dispatcher.utter_message(f"Type :n_correct_qs {type(n_correct_qs)}")
        # dispatcher.utter_message(f"Type :exercise_id {type(exercise_id)}")
        exercise_id = int(exercise_id) + 1
        sql2 = "SELECT question,Question_id FROM SQL_level WHERE level='%s' AND Question_id ='%s'" % (
            level_sql, exercise_id)
        try:
            # Execute the SQL Queryc
            mycursor.execute(sql2)
            results = mycursor.fetchall()

            for row in results:
                # dispatcher.utter_message(f"resuls[0] \n {row[0]} \n ")
                # dispatcher.utter_message(f"resuls[0] \n {row[1]} \n ")
                question = row[0]
                q_id = row[1]
                # dispatcher.utter_message( f"your level_sql is \n {level_sql} \n ")

                return question, q_id, level_sql, n_correct_qs
        except:
            dispatcher.utter_message("Error : Unable to fetch data.")

    if name == 'move_on':
        n = 0
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

                return question, q_id, level_sql, n

        except:
            dispatcher.utter_message("Error : Unable to fetch data.")


def dataCheckAnswer(answer, exercise_id, dispatcher, id, n_correct_qs):
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
                dispatcher.utter_message(f"Correct! Well done\n")
                dispatcher.utter_message(f"Answer: {answer}")

                reply2 = "Correct"
                n = n_correct_qs + 1
                return reply2, n

            else:
                # reply = "Hard luck " + name1 + ". Try again!"
                sql2 = answer
                try:
                    # Execute the SQL Query
                    mycursor.execute(sql2)
                    # results = mycursor.fetchall()
                    # err = mysql.connector.Error

                except mysql.connector.Error as err:
                    dispatcher.utter_message("Hmm looks like something went wrong, heres some feedback:\n")
                    # dispatcher.utter_message(err)
                    # dispatcher.utter_message(f"Error Code: {err.errno}")
                    dispatcher.utter_message(f"Message: {err.msg} \n")
                    dispatcher.utter_message(response="utter_show_answer")
                    reply2 = "Incorrect"
                    return reply2, n_correct_qs

                results2 = mycursor.fetchall()
                # print(results2)
                mycursor.execute(ans)
                results3 = mycursor.fetchall()
                # print(results3)
                difference = 0
                if len(results3) > 1:
                    for x, y in zip(results3, results2):
                        new_list = list(set(x).intersection(y))
                        new_list_diff = list(set(x).difference(y))
                        if len(new_list_diff) > 0:
                            difference = difference + 1
                    if difference == 0:
                        dispatcher.utter_message(f"Looks like this is correct! However I got a slightly different answer: {ans}")
                        reply2 = "Correct"
                        n = n_correct_qs + 1
                        return reply2, n
                    if difference > 0:
                        dispatcher.utter_message(f"Not quite... Try again!")
                        reply2 = "Incorrect"
                        return reply2, n_correct_qs

                # print(results3)
                if len(results3) == 1:
                    if results2 == results3:
                        dispatcher.utter_message(f"Looks like this is correct! However I got a slightly different answer: {ans}")
                        reply2 = "Correct"
                        n = n_correct_qs + 1
                        return reply2, n


    except:
        dispatcher.utter_message("Error : Unable to fetch data.")


def dataUpdateOnQuit(id, level, dispatcher, name, last_question_score):
    global level_s
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")
    mycursor = mydb.cursor()
    # get starting level
    sql2 = "SELECT level_sql FROM rasa_person WHERE id='%s'" % (id)
    try:
        # Execute the SQL Query
        mycursor.execute(sql2)
        results2 = mycursor.fetchall()

        for row in results2:
            level_s = row[0]

        dispatcher.utter_message("------ LESSON SUMMARY --------\n")
        dispatcher.utter_message("Types of questions attempted:\n")
        # qnamelist = []
        for i in range(level_s, level + 1):
            # dispatcher.utter_message(f">>level {level}")
            # dispatcher.utter_message(f" -------- i {i} --------")
            sql3 = "SELECT DISTINCT q_name FROM SQL_level WHERE level='%s' LIMIT 1" % (i)
            try:
                # Execute the SQL Query
                mycursor.execute(sql3)
                results3 = mycursor.fetchall()
                for rows in results3:
                    q_name = rows[0]
                    dispatcher.utter_message(f">> {q_name}")
                    # qnamelist = qnamelist.append(q_name)

            except:
                dispatcher.utter_message("Error : Unable to fetch data.1")

                # dispatcher.utter_message(f">> {q_name}")
        # final_new_qs = list(set(qnamelist))
        # for x in final_new_qs:
        #     dispatcher.utter_message(f">> {x}")
        dispatcher.utter_message("-------------------------\n")
    except:
        dispatcher.utter_message("Error : Unable to fetch data. 2")

    sql = "UPDATE rasa_person SET level_sql='%s',last_question_score='%s' WHERE id='%s'" % (
    level, last_question_score, id)
    mycursor.execute(sql)
    mydb.commit()
    dispatcher.utter_message(f" Bye {name}! I hope to see you again soon")


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
        if level == 4:
            dispatcher.utter_message(
                f" Remember you learned about using WHERE in a SELECT statement when conditions are involved? \n Try this syntax in your exercise: \n SELECT column1, column2 \n FROM table1 WHERE condition")
        if level == 5:
            dispatcher.utter_message(
                f" Remember you learned about WHERE with AND/OR/NOT in a SELECT statement when multiple conditions are involved? \n Try this syntax in your exercise: \n SELECT column1, column2 \n FROM table1 WHERE condition1 AND condition2")
        if level == 6:
            dispatcher.utter_message(
                f" Remember you learned about WHERE with AND/OR/NOT in a SELECT statement when multiple conditions are involved? \n Try this syntax in your exercise: \n SELECT column1, column2 \n FROM table1 WHERE condition1 AND (condition2 OR condition3)")

    elif 'theory' in msg:
        if level == 1:
            dispatcher.utter_message(
                f" Remember you learned about the SELECT statement?  \n SELECT - extracts data from a database.")
        if level == 2:
            dispatcher.utter_message(
                f" Remember you learned about the SELECT * statement?  \n SELECT * - returns all values in a table.")
        if level == 3:
            dispatcher.utter_message(
                f" Remember you learned about the SELECT DISTINCT statement? \n The SELECT DISTINCT statement is used to return only distinct (different) values. \n Inside a table, a column often contains many duplicate values and sometimes you only want to list the different (distinct) values.")
        if level == 4:
            dispatcher.utter_message(
                f" Remember you learned about using WHERE in a SELECT statement when conditions are involved? \n Including WHERE in a SELECT statement allows us to include conditions in the query. \n These conditions can include using =, <, > ")
        if level == 5:
            dispatcher.utter_message(
                f" Remember you learned about WHERE with AND/OR/NOT in a SELECT statement when multiple conditions are involved? \n We use WHERE with AND when there are multiple conditions involved so that all conditions \n can be accounted for.")
        if level == 6:
            dispatcher.utter_message(
                f" Remember you learned about WHERE with AND/OR/NOT in a SELECT statement when multiple conditions are involved? \n In this question more than one type of operator is used. \n This means there are more than 2 conditions which use a combination of operators. \n For example AND with OR..")

    else:
        if level == 1:
            dispatcher.utter_message(
                f" Remember you learned about the SELECT statement? \n Try this syntax in your exercise: \n SELECT column1, column2  \n FROM table_name;")
        if level == 2:
            dispatcher.utter_message(
                f" Remember you learned about the SELECT statement? \n Try this syntax in your exercise: \n SELECT * FROM table_name;")
        if level == 3:
            dispatcher.utter_message(
                f" Remember you learned about the SELECT DISTINCT statement? \n Try this syntax in your exercise: \n SELECT DISTINCT column1, column2 \n FROM table_name;")
        if level == 4:
            dispatcher.utter_message(
                f" Remember you learned about using WHERE in a SELECT statement when conditions are involved? \n Try this syntax in your exercise: \n SELECT column1, column2 \n FROM table1 WHERE condition")
        if level == 5:
            dispatcher.utter_message(
                f" Remember you learned about WHERE with AND/OR/NOT in a SELECT statement when multiple conditions are involved? \n Try this syntax in your exercise: \n SELECT column1, column2 \n FROM table1 WHERE condition1 AND condition2")
        if level == 6:
            dispatcher.utter_message(
                f" Remember you learned about WHERE with AND/OR/NOT in a SELECT statement when multiple conditions are involved? \n Try this syntax in your exercise: \n SELECT column1, column2 \n FROM table1 WHERE condition1 AND (condition2 OR condition3)")


def FirstTimeQustion(dispatcher):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")
    mycursor = mydb.cursor()
    sql2 = "SELECT question,Question_id, q_name FROM SQL_level WHERE level='1' AND Question_id ='1'"
    try:
        # Execute the SQL Query
        mycursor.execute(sql2)
        results = mycursor.fetchall()

        for row in results:
            # dispatcher.utter_message(f"resuls[0] \n {row[0]} \n ")
            # dispatcher.utter_message(f"resuls[0] \n {row[1]} \n ")
            question = row[0]
            q_id = row[1]
            qname = row[2]
            # dispatcher.utter_message( f"your level_sql is \n {level_sql} \n ")

            return question, q_id,qname
    except:
        dispatcher.utter_message("Error : Unable to fetch data.")


def dataShowAnswer( dispatcher, e_id):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")

    mycursor = mydb.cursor()
    # mycursor_name = mydb.cursor()
    sql = "SELECT answer,question FROM SQL_level WHERE Question_id='%s'" % (e_id)
    try:
        # Execute the SQL Query
        mycursor.execute(sql)
        results = mycursor.fetchall()

        for row in results:
            # dispatcher.utter_message(f"resuls[0] \n {row[0]} \n ")
            # dispatcher.utter_message(f"resuls[0] \n {row[1]} \n ")
            answer = row[0]
            question = row[1]

            dispatcher.utter_message(f"The answer to: '  {question}  ' is: \n ")
            dispatcher.utter_message(f" {answer} ")

    except:
        dispatcher.utter_message("Error : Unable to fetch data.")
