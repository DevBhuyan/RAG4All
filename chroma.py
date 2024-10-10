#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 20 02:47:54 2024

@author: dev
"""

import os
from hf_llm import hf_embed
import json
import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import chromadb


chroma_client = chromadb.Client()


INDEX_NAME = "data"

COLLECTION = chroma_client.get_or_create_collection(name=INDEX_NAME)


def insert(docs_with_chunk_ids: list[tuple[str, str]]):

    existing_chunk_ids = COLLECTION.get()["ids"]

    docs, chunk_ids, product_ids = [], [], []
    for doc_w_id in docs_with_chunk_ids:
        if doc_w_id[1] not in existing_chunk_ids:
            docs.append(doc_w_id[0])
            chunk_ids.append(doc_w_id[1])
            product_ids.append({"product_id": doc_w_id[2]})

    if len(docs):
        print("Generating Embeddings")
        embeddings = hf_embed(docs)

        print("Adding to collection")
        COLLECTION.add(
            documents=docs,
            embeddings=embeddings,
            ids=chunk_ids,
            metadatas=product_ids
        )

        print("Added documents with chunk_ids: ", chunk_ids)
    else:
        print("No more elements to add")


def query_top_n(doc: str,
                n: int = 5):

    embedding = hf_embed(doc)
    
    if isinstance(embedding, dict):
        print(embedding)
        raise Exception("Rate limit reached, please try after 60 minutes.")

    results = COLLECTION.query(embedding, n_results=n)
    return results["documents"][0], results["ids"][0]


def load_faq_to_chroma():

    for file in os.listdir('./datafeed'):
        if file.endswith('.json'):
            with open(f'./datafeed/{file}', 'r') as f:
                contents = json.load(f)

            docs_with_ids = [
                (doc["context"],
                 str(doc["id"])) for doc in contents
            ]

            insert(docs_with_ids)


if __name__ == "__main__":
    load_faq_to_chroma()
