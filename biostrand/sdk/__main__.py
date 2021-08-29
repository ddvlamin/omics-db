"""
"""

import logging
import json

import requests
import h5py

PROTOCOL = "http"

class VectorClient():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__connection_str = f"{self.__host}:{self.__port}/"

    def __call_api(self, endpoint, method="GET", protocol=PROTOCOL, encoding="utf-8", request_body=None):
        url = protocol + "://" + self.__connection_str + endpoint

        if request_body != None:
            data = json.dumps(request_body).encode('ascii') # data should be bytes
            headers = {"Content-Type": "application/json"}
        else:
            data = None
            headers = {}

        if method == "GET":
            response = requests.get(url, headers=headers)
        elif method == "POST":
            response = requests.post(url, data=data, headers=headers)
        else:
            raise ValueError(f"method {method} not supported")

        if response.status_code != requests.codes.ok:
            logging.error(f"An error occured with code {response.status_code}, contact Biostrand and provide your query")
            return {}

        json_response = response.json()

        return json_response

    def get_similar_sequences(self, query_vector, top=5000, collection="pdb"):
        """
        """
        endpoint = "query"
        request_body = {"query_vector": query_vector, "collection": collection, "top": top}
        sequences = self.__call_api(endpoint, method="POST", request_body=request_body)

        return sequences


if __name__ == "__main__":
    query_file = "../../data/2.60.40.10.h5"
    query_vector = [float(i) for i in h5py.File(query_file, 'r')["3kdmA02"]]

    client = VectorClient(host="localhost", port=9001)
    response = client.get_similar_sequences(query_vector, top=10)
    print(json.dumps(response, indent=2))