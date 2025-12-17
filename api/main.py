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
    top_k: int = 10


class Assessment(BaseModel):
    assessment_name: str
    assessment_url: str


class RecommendResponse(BaseModel):
    recommendations: List[Assessment]


#endpoints

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    results = retrieve_assessments(req.query, top_k=req.top_k)

    if not results:
        raise HTTPException(
            status_code=404,
            detail="No relevant assessments found"
        )

    recommendations = [
        {
            "assessment_name": r["name"],
            "assessment_url": r["url"]
        }
        for r in results
    ]

    return {"recommendations": recommendations}



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
