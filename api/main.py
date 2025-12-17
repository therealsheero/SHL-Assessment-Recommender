from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request


from recommender.retrieve import retrieve_assessments

app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0"
)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
templates = Jinja2Templates(directory="frontend/templates")

#request / response schemas

class RecommendRequest(BaseModel):
    query: str

#endpoints

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/recommend")
def recommend(req: RecommendRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    results = retrieve_assessments(req.query, top_k=10)

    formatted = []
    for r in results:
        formatted.append({
            "url": r["url"],
            "name": r["name"],
            "adaptive_support": r.get("adaptive_irt", "No"),
            "description": r.get("description", ""),
            "duration": int(r.get("assessment_length", 0)) if str(r.get("assessment_length", "")).isdigit() else 0,
            "remote_support": r.get("remote_testing", "No"),
            "test_type": r["test_type"] if isinstance(r["test_type"], list) else [r["test_type"]]
        })

    return {
        "recommended_assessments": formatted
    }




@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": None}
    )

@app.post("/ui-recommend", response_class=HTMLResponse)
def ui_recommend(request: Request, query: str = Form(...)):
    results = retrieve_assessments(query, top_k=10)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "query": query, "results": results}
    )
