import sys
import argparse

from pymilvus_orm import connections, FieldSchema, CollectionSchema, DataType, Collection
import h5py
import pymilvus_orm

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='load omics vectors into vector database')
    parser.add_argument('file', type=str, help='file to load')
    parser.add_argument('--host', type=str, default="localhost", help='db host')
    parser.add_argument('--port', type=str, default="19530", help='db port')
    parser.add_argument('--dim', type=int, default=6165, help='number of dimensions of the embedding vectors')
    parser.add_argument('--collection', type=str, default="pdb", help='name of the collection')
    args = parser.parse_args()

    dim = args.dim
    collection_name = args.collection

    f = h5py.File(args.file, 'r')

    connections.connect(host=args.host, port=args.port)
    fields = [
        FieldSchema(name="enumerate_id", dtype=DataType.INT64, is_primary=True),
        FieldSchema(name="sequence_vector", dtype=DataType.FLOAT_VECTOR, dim=dim)
    ]
    schema = CollectionSchema(fields=fields, description="omics vectors")
    collection = Collection(name=collection_name, schema=schema)

    batch = [[],[]]
    for j, key in enumerate(f.keys()):
        batch[0].append(j)
        batch[1].append([float(i) for i in f[key]])
        if len(batch[0]) >= 1000:
            collection.insert(batch)
            batch = [[],[]]
            print(j)

    collection.create_index(field_name="sequence_vector",
                            index_params={'index_type': 'IVF_FLAT',
                                          'metric_type': 'IP',
                                          'params': {
                                            'nlist': 100      # int. 1~65536
                                          }})



    connections.get_connection("default").flush([collection_name])

    print(f"collections: {connections.get_connection('default').list_collections()}")
    print(f"number of records: {collection.num_entities}")
