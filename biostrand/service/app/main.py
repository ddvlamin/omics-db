import logging
import os
import json

from fastapi import FastAPI
from typing import Optional, List
from fastapi.logger import logger
from pydantic import BaseModel

from pymilvus_orm import connections, Collection
from sklearn.preprocessing import normalize

DBHOST = "localhost"
DBPORT = "19530"
COLLECTION = "pdb"

logger.setLevel(logging.INFO)
logging.root = logger
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

app = FastAPI()

class QueryRequest(BaseModel):
    query_vector: List[float]
    top: Optional[int] = 5000
    nprobe: Optional[int] = 10

@app.on_event("startup")
async def startup_event():
    connections.connect(host=DBHOST, port=DBPORT)
    app.collection = Collection(name=COLLECTION)
    app.collection.load()
    logging.info("loaded vector collection")

    app.metadata = {}
    with open("data/index2id.json", "r") as fin:
        app.metadata.update(json.load(fin))

@app.get("/health")
def root():
    return {}

@app.post("/query")
def get_similar_sequences(request: QueryRequest):
    """
    """
    search_params = {"metric_type": "IP", "params": {"nprobe": request.nprobe}}

    query_vector = np.array(request.query_vector).reshape(-1,1)
    query_vector = normalize(query_vector).flatten().tolist()
    candidate_hits = app.collection.search([query_vector], "sequence_vector", search_params, request.top, "", output_fields=["id"])

    result = {}
    for candidate in candidate_hits:
        for id, dis in zip(candidate.ids, candidate.distances):
            sequence_id = app.metadata.get(str(id))
            if sequence_id is not None:
                result[sequence_id] = dis

    return result

