from typing import Union

from fastapi import FastAPI, Request, Depends, Form, status
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)#what it does

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse("base.html",{"request": request, "todos_list":todos})

@app.post("/add")
def add(request:Request, title: str= Form(...), db: Session = Depends(get_db)):
    new_todo = models.Todo(title=title)
    db.add(new_todo)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)