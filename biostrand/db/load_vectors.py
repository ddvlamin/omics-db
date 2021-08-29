import argparse
import os

from pymilvus_orm import connections, Collection
import numpy as np
from sklearn.preprocessing import normalize

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='load omics vectors into vector database')
    parser.add_argument('basepath', type=str, help='file to load')
    parser.add_argument('--fileprefix', type=str, default="index2id", help='template name of file')
    parser.add_argument('--host', type=str, default="localhost", help='db host')
    parser.add_argument('--port', type=str, default="19530", help='db port')
    parser.add_argument('--dim', type=int, default=6165, help='number of dimensions of the embedding vectors')
    parser.add_argument('--nfiles', type=int, default=581, help='number of files to load')
    parser.add_argument('--blocksize', type=int, default=1000, help='number of vectors in one file')
    parser.add_argument('--collection', type=str, default="pdb", help='name of the collection')
    args = parser.parse_args()

    block_size = args.blocksize
    nfiles = args.nfiles
    dim = args.dim
    collection_name = args.collection

    connections.connect(host=args.host, port=args.port)
    collection = Collection(name=collection_name)

    stop = 0
    for fileindex in range(1,nfiles+1):
        filepath = os.path.join(args.basepath, f"{args.fileprefix}_{fileindex}.npy")
        vectors = np.load(filepath)
        if vectors.shape[0] != block_size:
            print(f"{filepath} has less than {block_size} vectors: {vectors.shape}")
        vectors = normalize(vectors)
        vectors = vectors.tolist()

        start = stop
        stop = start+len(vectors)
        ids = [i for i in range(start, stop)]

        collection.insert([ids, vectors])
        connections.get_connection("default").flush([collection_name])

        print(f"loaded {filepath}")

    print(f"collections: {connections.get_connection('default').list_collections()}")
    print(f"number of records: {collection.num_entities}")
    print(f"last id: {stop-1}")

    connections.disconnect("default")