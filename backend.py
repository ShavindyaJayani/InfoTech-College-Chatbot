from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import chromadb
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import re


app = FastAPI(title="InfoTech College Chatbot API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="infotech_college")


vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    sources: list

@app.get("/")
def read_root():
    return {"message": "InfoTech College Chatbot API is running"}

def get_tfidf_embedding(text):
    """Generate TF-IDF embedding for text"""
    try:
        embedding = vectorizer.transform([text]).toarray()[0]
        return embedding
    except:
        
        return np.zeros(5000)

def extract_relevant_info(query, documents):
    """Extract relevant information based on the query"""
    query_lower = query.lower()
    
    
    relevant_info = []
    
    for doc in documents:
        doc_lower = doc.lower()
        
        if "program" in query_lower or "course" in query_lower:
            if "fit" in doc_lower or "foundation" in doc_lower:
                relevant_info.append(doc)
        
        elif "tuition" in query_lower or "cost" in query_lower or "fee" in query_lower or "payment" in query_lower:
            if "payment" in doc_lower or "fee" in doc_lower or "rs." in doc_lower or "registration" in doc_lower:
                relevant_info.append(doc)
        
        elif "contact" in query_lower or "email" in query_lower or "phone" in query_lower:
            if "contact" in doc_lower or "email" in doc_lower or "phone" in doc_lower:
                relevant_info.append(doc)
        
        elif "admission" in query_lower or "apply" in query_lower or "requirement" in query_lower:
            if "admission" in doc_lower or "apply" in doc_lower or "requirement" in doc_lower:
                relevant_info.append(doc)
        
        elif "duration" in query_lower or "length" in query_lower or "month" in query_lower:
            if "month" in doc_lower or "duration" in doc_lower:
                relevant_info.append(doc)
        
        else:
            
            relevant_info.append(doc)
    
    return relevant_info

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        
        all_docs = collection.get()
        documents = all_docs['documents']
        
        
        if not hasattr(vectorizer, 'vocabulary_'):
            vectorizer.fit(documents)
        
        
        query_embedding = get_tfidf_embedding(request.message)
        
        
        similarities = []
        for doc in documents:
            doc_embedding = get_tfidf_embedding(doc)
            similarity = cosine_similarity([query_embedding], [doc_embedding])[0][0]
            similarities.append(similarity)
        
        
        top_indices = np.argsort(similarities)[-3:][::-1]
        
        
        context_parts = []
        sources = []
        for idx in top_indices:
            if similarities[idx] > 0.1:  
                clean_doc = documents[idx]
                clean_doc = clean_doc.replace("FIT HANDBOOK 2025 INFOTECH COLLEGE", "")
                clean_doc = re.sub(r'Page \d+ of \d+', '', clean_doc)
                clean_doc = ' '.join(clean_doc.split())
                
                if clean_doc not in context_parts:
                    context_parts.append(clean_doc)
                    sources.append(all_docs['metadatas'][idx]['source'])
        
        
        relevant_info = extract_relevant_info(request.message, context_parts)
        
        
        if relevant_info:
            
            combined_info = " ".join(relevant_info[:2]) 
            
           
            if len(combined_info) > 500:
                response = f"{combined_info[:500]}... [More information available in documents]"
            else:
                response = combined_info
        else:
            response = "I couldn't find specific information about that topic in the available documents. Please try asking about programs, fees, admissions, or contact information."
        
        
        sources = list(set(sources))
        
        return ChatResponse(response=response, sources=sources)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)