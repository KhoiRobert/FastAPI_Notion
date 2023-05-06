from typing import Union

from fastapi import FastAPI, Request, Depends, Form, status
from starlette.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)#1

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")#2

def get_db():#3
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close

@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):#4
    todos = db.query(models.Todo).all()
    return templates.TemplateResponse("base.html",{"request": request, "todo_list":todos})#5

@app.post("/add")
def add(request: Request, title: str = Form(...), db: Session = Depends(get_db)):
    new_todo = models.Todo(title=title)
    db.add(new_todo)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)#6

@app.get("/update/{todo_id}")
def update(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()#7
    todo.complete = not todo.complete
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)


@app.get("/delete/{todo_id}")
def delete(request: Request, todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    db.delete(todo)
    db.commit()

    url = app.url_path_for("home")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)