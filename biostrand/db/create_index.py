import argparse

from pymilvus_orm import connections, Collection

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create index on vector embedding')
    parser.add_argument('--host', type=str, default="localhost", help='db host')
    parser.add_argument('--port', type=str, default="19530", help='db port')
    parser.add_argument('--collection', type=str, default="pdb", help='name of the collection')
    args = parser.parse_args()

    connections.connect(host=args.host, port=args.port)
    collection = Collection(name=args.collection)

    collection.create_index(field_name="sequence_vector",
                            index_params={'index_type': 'IVF_PQ',
                                          'metric_type': 'IP',
                                          'params': {
                                              'nlist': 100,      # int. 1~65536
                                              'm': 8
                                          }})

    print(f"collections: {connections.get_connection('default').list_collections()}")
    print(f"number of records: {collection.num_entities}")
