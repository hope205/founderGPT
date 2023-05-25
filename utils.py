import os
import openai
import requests
from dotenv import load_dotenv
import pinecone
import streamlit as st

load_dotenv()





PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
PINECONE_API_ENV = st.secrets["PINECONE_API_ENV"]
openai.api_key = st.secrets["AI_API_KEY"]





    
    
    # initialize pinecone
pinecone.init(
api_key=PINECONE_API_KEY,  # find at app.pinecone.io
environment=PINECONE_API_ENV  # next to api key in console
)




index =pinecone.Index("foundergpt")

# Get embeddings for a given string
def get_embeddings_openai(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    response = response['data']

    # extract embeddings from responses0
    return [x["embedding"] for x in response]


# Search Pinecone for similar documents
def semantic_search(query, **kwargs):
    # Embed the query into a vector
    v = get_embeddings_openai(query)
    
    
    # retrieve from Pinecone
    # xq = v['data'][0]['embedding']
    xq = v
    

    # get relevant contexts
    res = index.query(xq, top_k=3, include_metadata=True)
    contexts = [
        x['metadata']['text'] for x in res['matches']
    ]
    
    return contexts
    
    

   
