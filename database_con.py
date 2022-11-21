import mysql.connector
import pymysql.cursors


def DataUpdate(name, Email,dispatcher):
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
            dispatcher.utter_message(f"User Name: {name}")
            dispatcher.utter_message(response="utter_response", name=name)
    except:
        dispatcher.utter_message("Error : Unable to fetch data.")


def dataGetId(name,Email,dispatcher):
    mydb = mysql.connector.connect(host="localhost", user="root",
                                   passwd="cremore23", database="Rasa_feedback")

    mycursor = mydb.cursor()
    sql = "SELECT id FROM rasa_person WHERE name='%s' AND Email='%s'" % (name,Email)

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
