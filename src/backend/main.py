# from typing import Union

import psycopg
from fastapi import FastAPI
from pydantic import BaseModel

import env
import utils


app = FastAPI()


class QueryBody(BaseModel):
    query: str
    commit: bool = False


@app.post("/query")
async def run_query(data: QueryBody):
    query_results = []
    colnames = []

    query = data.query.strip()

    if not query:
        return {"columns": [], "results": []}

    async with await psycopg.AsyncConnection.connect(env.DB_URI) as conn:
        async with conn.cursor() as cursor:
            query = utils.parse_query(query)

            await cursor.execute(query)

            if data.commit:
                await conn.commit()

            if cursor.description:
                colnames = utils.get_colnames(cursor)

                # convert the output into a list of dictionaries of {column_name: value}
                query_results = [row async for row in cursor]

    return {
        "columns": colnames,
        "results": query_results,
    }
