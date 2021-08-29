import logging
import os
import json

from fastapi import FastAPI
from typing import Optional, List
from fastapi.logger import logger
from pydantic import BaseModel

from pymilvus_orm import connections, Collection

DBHOST = "localhost"
DBPORT = "19530"
METADATA = {}

logger.setLevel(logging.INFO)
logging.root = logger
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging.basicConfig(level=LOGLEVEL)

app = FastAPI()

class QueryRequest(BaseModel):
    query_vector: List[float]
    collection: Optional[str] = "pdb"
    top: Optional[int] = 5000
    nprobe: Optional[int] = 10

@app.on_event("startup")
async def startup_event():
    with open("data/index2id.json", "r") as fin:
        METADATA.update(json.load(fin))

@app.get("/health")
def root():
    return {}

@app.post("/query")
def get_similar_sequences(request: QueryRequest):
    """
    """
    search_params = {"metric_type": "IP", "params": {"nprobe": request.nprobe}}

    connections.connect(host=DBHOST, port=DBPORT)
    collection = Collection(name=request.collection)
    collection.load()

    candidate_hits = collection.search([request.query_vector], "sequence_vector", search_params, request.top, "", output_fields=["id"])

    result = {}
    for candidate in candidate_hits:
        for id, dis in zip(candidate.ids, candidate.distances):
            sequence_id = METADATA.get(str(id))
            if sequence_id is not None:
                result[sequence_id] = dis

    return result

