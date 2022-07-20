from fastapi import FastAPI
import uvicorn
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


from driver import CassandraDriver

HOST = os.environ.get('CASSANDRA_HOST', 'localhost')
PORT = os.environ.get('CASSANDRA_PORT', 9042)
KEYSPACE = os.environ['KEYSPACE']
TABLE = os.environ['TABLE']


cd = CassandraDriver(HOST, PORT, KEYSPACE)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/data")
async def get_data():
    data = cd.get_all_data(TABLE)
    print(data)
    return "Hello World"
    # return data







if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9015)
