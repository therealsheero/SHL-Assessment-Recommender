from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

from recommender.retrieve import retrieve_assessments

app = FastAPI(title="SHL Assessment Recommendation Web App")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

templates = Jinja2Templates(directory="frontend/templates")



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": None}
    )


@app.post("/recommend", response_class=HTMLResponse)
def recommend(request: Request, query: str = Form(...)):
    results = retrieve_assessments(query, top_k=10)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "query": query,
            "results": results
        }
    )
