from fastapi import FastAPI
import uvicorn
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


from driver import CassandraDriver

HOST = os.environ.get('CASSANDRA_HOST', 'localhost')
PORT = os.environ.get('CASSANDRA_PORT', 9042)
KEYSPACE = os.environ['KEYSPACE']
OFFLINE_TABLE = os.environ['OFFLINE_TABLE']

cd = CassandraDriver(HOST, PORT, KEYSPACE)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World", "status_code": 200}

@app.get("/health")
async def health():
    return {"message": "OK", "status_code": 200}

@app.get("/data")
async def get_data():
    raw_data = cd.get_all_data(OFFLINE_TABLE)
    data = {'text': [], 'author_id': [], 'topic': []}
    for row in raw_data:
        data['author_id'].append(row.author_id)
        data['text'].append(row.text)
        data['topic'].append(row.topic)

    return json.dumps(data)






if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9015)
