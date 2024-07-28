
import pandas as pd
import chromadb
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from chromadb.utils import embedding_functions
from langchain_chroma import Chroma
from langchain.prompts import PromptTemplate 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import LLMChain
from client_chatbot import *

def read_data(dau_vao):
    client = chromadb.HttpClient(host='localhost', port=8000)
    embeddings = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    db = client.get_collection(name="QA_collection", embedding_function=embeddings)
    dau_vao1 = str(dau_vao)
    results = db.query(
        query_texts=[dau_vao1],
        n_results=3
    )
    QandA_Prompt = PromptTemplate(
    input_variables=["text","query"],
    template="Bạn là một chuyên gia trong các dịch vụ ngân hàng và cung cấp thông tin chính xác bằng đoạn văn dưới đây. \
    Câu trả lời của bạn nên chi tiết nhưng đơn giản, đảm bảo khách hàng hiểu tất cả các khía cạnh. \
    Giữ giọng điệu thân thiện và tránh các thuật ngữ kỹ thuật.\
    Câu hỏi: {query}\
    Nội dung: {text}"
    )
    LLM = ChatGoogleGenerativeAI(temperature=0.8, model="gemini-pro")
    output_chain = LLMChain(llm=LLM, prompt=QandA_Prompt)
    dauraresult = output_chain.run(query= dau_vao1,text=results)
    daura_text = dauraresult['text'] if isinstance(dauraresult, dict) else dauraresult
    return daura_text