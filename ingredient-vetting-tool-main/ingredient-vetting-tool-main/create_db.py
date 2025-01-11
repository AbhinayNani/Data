import os
import argparse
import faiss
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
import pandas as pd
from langchain_core.documents import Document

def create_new_vectorstore():
    load_dotenv()
    os.environ["GOOGLE_API_KEY"] = "AIzaSyAFRtlvbZCNiZJYZryYslw9lEqEsYgdgs0"

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    index = faiss.IndexFlatL2(len(embeddings.embed_query("hello world")))

    vector_store = FAISS(
        embedding_function=embeddings,
        index=index,
        docstore=InMemoryDocstore(),
        index_to_docstore_id={},
    )

    df = pd.read_csv("dataset.csv", header=0)

    docs = []
    ids = df['id'].tolist()

    for _, row in df.iterrows():
        document = Document(
            page_content=row['description'],
            metadata={"name": row['name']}
        )
        docs.append(document)

    vector_store.add_documents(documents=docs, ids=list(map(str, ids)))

    vector_store.save_local("database")

create_new_vectorstore()