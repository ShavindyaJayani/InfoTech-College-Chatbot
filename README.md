# InfoTech College Chatbot 

A Retrieval-Augmented Generation (RAG) chatbot for InfoTech College website, built with FastAPI backend and Streamlit frontend. This project implements a question-answering system that can extract information from college documents and provide accurate responses.

## Features

- RAG Architecture: Uses vector database for efficient information retrieval
- FastAPI Backend: RESTful API for chatbot functionality
- Streamlit Frontend: User-friendly web interface
- Document Processing: Extracts and processes information from PDF documents
- Local Processing: No external API costs (uses TF-IDF and cosine similarity)

## Architecture
Infotech-Chatbot/
├── backend.py # FastAPI backend server
├── frontend.py # Streamlit frontend interface
├── requirements.txt # Python dependencies
├── chroma_db/ # Vector database (auto-generated)
├── data/ # PDF documents directory
└── README.md # Project documentation


##Prerequisites

- Python 3.8+
- pip (Python package manager)
- PDF documents in the `data/` folder

##Installation

1. Clone the repository:
   ```bash
git clone https://github.com/your-username/infotech-chatbot.git
cd infotech-chatbot
 Key Features Implemented
Required Features
RAG (Retrieval Augmented Generation) architecture

Vector database (ChromaDB) for document storage and retrieval

LLM-based question answering system

Document processing from PDF files

Optional Features
FastAPI backend with RESTful endpoints

Streamlit web frontend

Interactive chat interface

Source attribution for responses

How It Works
Document Processing: PDF files are loaded and split into chunks

Vectorization: Text chunks are converted to vectors using TF-IDF

Storage: Vectors are stored in ChromaDB vector database

Query Processing: User questions are vectorized and matched against stored documents

Response Generation: Most relevant document chunks are returned as answers

Deployment
Local Deployment
bash
# Terminal 1 - Start backend
python backend.py

# Terminal 2 - Start frontend  
streamlit run frontend.py

Acknowledgments
InfoTech College for providing the document data

FastAPI and Streamlit communities for excellent documentation

ChromaDB team for the vector database solution


cd infotech-chatbot
