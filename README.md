# SHL Assessment Recommendation System

This project implements an intelligent assessment recommendation system for SHL,
using Retrieval-Augmented Generation (RAG) techniques.

## Features
- Scrapes SHL assessment catalog (377+ individual tests)
- Semantic search using Sentence Transformers + FAISS
- Balanced recommendations across skill types
- REST API using FastAPI
- Web frontend for interactive querying
- Evaluation using Mean Recall@10

## Tech Stack
- Python
- FastAPI
- SentenceTransformers
- FAISS
- Pandas
- Jinja2
- HTML/CSS

## API Endpoints
- `GET /health`
- `POST /recommend`
- `GET /docs`

## Running Locally
```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
