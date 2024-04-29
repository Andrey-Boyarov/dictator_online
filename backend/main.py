import time

from random import randrange

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from db_connector import DbConnector


reconnect_attempt_number = 10
conn = DbConnector(timeout=reconnect_attempt_number)


async def find_random_question(faction: str, sess: AsyncSession) -> str:
    return await sess.execute(text(f"""
        select 
            id, 
            prompt 
        from 
            questions 
        where 
            faction = '{faction}'
            and 
            active is true 
        order by 
            random() 
        limit 1
    """))


async def find_result(id: int, answer: bool) -> str:
    if answer:
        return await find_confirmation_result(id=id)
    return await find_rejection_result(id=id)

# id, prompt, faction,
# confirm_crowd, confirm_oligarchs, confirm_enforcment, confirm_lawyers, confirm_army, confirm_mafia,
# reject_crowd, reject_oligarchs, reject_enforcment, reject_lawyers, reject_army, reject_mafia,
# active
async def find_confirmation_result(id: int, sess: AsyncSession):
    return await sess.execute(text(f"""
        select 
            confirm_crowd, 
            confirm_oligarchs, 
            confirm_enforcment, 
            confirm_lawyers, 
            confirm_army, 
            confirm_mafia 
        from 
            questions 
        where 
            id = {id} 
            and 
            active is true
    """)).fetchone()

async def find_rejection_result(id: int, sess: AsyncSession):
    return sess.execute(text(f"""
        select 
            reject_crowd, 
            reject_oligarchs, 
            reject_enforcment, 
            reject_lawyers, 
            reject_army, 
            reject_mafia 
        from 
            questions 
        where 
            id = {id}
            and 
            active is true
    """)).fetchone()


app = FastAPI()


@app.get("/question/{faction}")
async def get_question(faction: str):
    global conn
    async with conn.create_async_session() as sess:
        return await find_random_question(faction=faction, sess=sess)


@app.get("/result/{id}/{answer}")
async def get_question(id: int, answer: bool):
    global conn
    async with conn.create_async_session() as sess:
        return await find_result(id=id, answer=answer, sess=sess)
