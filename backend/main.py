from fastapi import FastAPI
from random import randrange

import psycopg2
import time

conn = None
reconnect_attempt_number = 10

async def connection_cursor():
    global conn

    for i in range(reconnect_attempt_number):
        try:
            if conn is None:
                print("DB CONNECTION IS NOT INITIALIZED")
                raise Exception("DB CONNECTION IS NONE")
            return conn.cursor()
        except (psycopg2.DatabaseError, Exception) as error:
            try:
                print("TRYING TO INITIALIZE DB CONNECTION")
                conn = psycopg2.connect(database="gigachad",
                                        host="gigachad-db",
                                        user="admin",
                                        password="admin",
                                        port="5432")
                print("DB IS CONNECTED")

                return conn.cursor()
            except (psycopg2.DatabaseError, Exception) as error:
                print("DB IS NOT CONNECTED YET (ATTEMPT {}):".format(i))
                print(error)
                if reconnect_attempt_number > i + 1:
                    print("GONNA TRY TO RECONNECT")
                else:
                    print("THAT WAS LAST ONE")
                time.sleep(5)

async def find_random_question(fraction: str):
    cur = await connection_cursor()
    cur.execute("select count(*) from questions where fraction = {0} and is_relevant is true".format(fraction))
    total = cur.fetchone()
    index = randrange(total)

    cur.execute("select id, prompt from questions where fraction = {0} and is_relevant is true limit 1 offset {1}".format(fraction, index))
    return cur.fetchone()

async def find_result(id: int, answer: bool):
    if answer:
        return await find_confirmation_result(id=id)
    return await find_rejection_result(id=id)

# id, prompt, 
# confirm_crowd, confirm_oligarchs, confirm_enforcment, confirm_lawyers, confirm_army, confirm_mafia,
# reject_crowd, reject_oligarchs, reject_enforcment, reject_lawyers, reject_army, reject_mafia,
# is_relevant
async def find_confirmation_result(id: int):
    cur = await connection_cursor()
    cur.execute("select confirm_crowd, confirm_oligarchs, confirm_enforcment, confirm_lawyers, confirm_army, confirm_mafia from questions where id = {} and is_relevant is true".format(id))
    return cur.fetchone()

async def find_rejection_result(id: int):
    cur = await connection_cursor()
    cur.execute("select reject_crowd, reject_oligarchs, reject_enforcment, reject_lawyers, reject_army, reject_mafia from questions where id = {} and is_relevant is true".format(id))
    return cur.fetchone()

app = FastAPI()

@app.get("/question/{fraction}")
async def get_question(fraction: str):
    return await find_random_question(fraction=fraction)

@app.get("/result/{id}/{answer}")
async def get_question(id: int, answer: bool):
    return await find_result(id=id, answer=answer)
