import argparse

from pymilvus_orm import connections, FieldSchema, CollectionSchema, DataType, Collection

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='create collection in vector database')
    parser.add_argument('--host', type=str, default="localhost", help='db host')
    parser.add_argument('--port', type=str, default="19530", help='db port')
    parser.add_argument('--dim', type=int, default=6165, help='number of dimensions of the embedding vectors')
    parser.add_argument('--collection', type=str, default="pdb", help='name of the collection')
    args = parser.parse_args()

    dim = args.dim
    collection_name = args.collection

    connections.connect(host=args.host, port=args.port)
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False),
        FieldSchema(name="sequence_vector", dtype=DataType.FLOAT_VECTOR, dim=dim)
    ]
    schema = CollectionSchema(fields=fields, description="omics vectors")
    collection = Collection(name=collection_name, schema=schema)
    connections.get_connection("default").flush([collection_name])

    print(f"collections: {connections.get_connection('default').list_collections()}")
    print(f"number of records: {collection.num_entities}")
