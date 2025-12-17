# SHL Assessment Recommendation System

An intelligent, retrieval-augmented recommendation system that maps natural language job descriptions to the most relevant SHL assessments.  
The system is designed to help hiring managers and recruiters quickly identify appropriate individual test solutions based on role requirements, skills, and competencies.

---

## Problem Overview

Hiring teams often rely on keyword-based search and manual filtering to select assessments, which is time-consuming and error-prone.  
This project builds a **semantic search–based recommendation system** that understands job descriptions and returns relevant SHL assessments in a structured and balanced manner.

---

## Key Features

- Semantic search over 389+ SHL Individual Test Solutions
- Job description input as free text (JD or query)
- Balanced recommendations across skill types (e.g. technical + behavioral)
- REST API compliant with SHL specifications
- Web-based UI for interactive testing
- Evaluation using Mean Recall@K

---

## System Architecture

```

Job Description / Query
↓
Sentence Embedding (SentenceTransformers)
↓
Vector Similarity Search (FAISS)
↓
Ranking Module
↓
Test-Type Balancing (K, P, C, etc.)
↓
Final Recommendations

```

---

## Tech Stack

### Core Technologies
- **Python**
- **FastAPI** – REST API framework
- **SentenceTransformers** – Semantic embeddings
- **FAISS** – Vector similarity search
- **Pandas / NumPy** – Data processing
- **Jinja2 + HTML/CSS** – Web frontend

---

## Why FAISS?

FAISS was chosen for:
- Fast and efficient semantic similarity search
- Lightweight deployment
- Deterministic retrieval behavior
- Easy integration with Python ML pipelines

This makes the system fully reproducible without external vector DB dependencies.

---

## Recommendation Pipeline

### 1. Data Ingestion
- Scraped SHL Product Catalog directly from shl.com
- Parsed and stored metadata such as:
  - Assessment name
  - Test type
  - Duration
  - Remote / adaptive support
  - Description
- Final dataset contains **389 unique Individual Test Solutions**

### 2. Embedding Generation
- Combined assessment name, description, and test type
- Generated dense embeddings using:
  - `all-MiniLM-L6-v2`

### 3. Retrieval
- FAISS index performs nearest-neighbor search
- Top-N candidates retrieved per query

### 4. Ranking
- Retrieved results are passed through a ranking module
- Current strategy preserves semantic similarity ordering
- Designed for easy extension (duration, job level, weighting)

### 5. Balancing
- Ensures diversity across test categories
- Example:
  - Knowledge & Skills
  - Personality & Behavior
  - Competencies
- Prevents over-representation of a single test type

---

## 🌐 API Endpoints

### Health Check
<img width="1920" height="970" alt="Screenshot (38)" src="https://github.com/user-attachments/assets/c35d8ae7-0537-41e1-9e03-4efb817a2357" />


### Recommendation Endpoint

```
POST /recommend
```

Request:

```json
{
  "query": "I am hiring a Java developer with good communication skills",
  "top_k": 5
}
```

Response:

```json
{
  "recommendations": [
    {
      "assessment_name": "Java Web Services (New)",
      "assessment_url": "https://www.shl.com/solutions/products/product-catalog/view/java-web-services-new/"
    }
  ]
}
```

---

## 🖥️ Web Application

* Simple frontend built using HTML, CSS, and Jinja2
* SHL-inspired color scheme
* Allows recruiters to:

  * Enter job descriptions
  * View recommended assessments instantly

The frontend is served from the same FastAPI application.

---

## 📈 Evaluation

The system is evaluated using **Mean Recall@10**, as required.

* Evaluation performed on the provided labeled training queries
* Demonstrates improvement through iterative tuning of:

  * Query representation
  * Balancing logic
  * Retrieval depth

Example output:

```
Mean Recall@10: 0.168
```

---

## 📂 Project Structure

```
SHL/
├── api/
│   └── main.py
├── recommender/
│   ├── retrieve.py
│   ├── rank.py
│   ├── balance.py
│   └── __init__.py
├── scraper/
│   └── crawl_shl.py
├── evaluation/
│   └── recall_atk.py
├── frontend/
│   ├── templates/
│   │   └── index.html
│   └── static/
├── embeddings/
│   └── faiss_index/
├── data/
│   └── raw/
├── requirements.txt
└── README.md
```

---

## ▶️ Running Locally

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload
```

Open:

* Web UI: `http://127.0.0.1:8000/`
* API Docs: `http://127.0.0.1:8000/docs`

---

## 🧪 Example Query

> “I am hiring a Java developer who can collaborate with business stakeholders.”

Returns a balanced mix of:

* Java technical assessments
* Communication / collaboration assessments

---

## 👤 Author

**Shreeya**
SHL GenAI Take-Home Assessment Submission

```
