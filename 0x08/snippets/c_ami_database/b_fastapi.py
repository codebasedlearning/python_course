"""
This snippet demonstrates a simple FastAPI-based To-Do REST API.

Teaching focus
  - FastAPI app setup
  - Pydantic data models
  - CRUD endpoints (GET, POST, DELETE)

Preparations
  - virtual environment activated and libs installed, here:
        pip install fastapi uvicorn

Usage
  - Run with: uvicorn b_fastapi:app --reload
  - Then open your browser and go to:
        http://127.0.0.1:8000/docs   -> Built-in Swagger UI
        http://127.0.0.1:8000/redoc  -> Alternative docs UI
"""

# pip install fastapi uvicorn

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Define a data model
class TodoItem(BaseModel):
    id: int
    task: str
    done: bool = False

# Fake database
todo_list: List[TodoItem] = []

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the To-Do API!"}

# Get all to-do items
@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    return todo_list

# Add a new to-do item
@app.post("/todos", response_model=TodoItem)
def create_todo(item: TodoItem):
    if any(existing.id == item.id for existing in todo_list):
        raise HTTPException(status_code=400, detail="ID already exists.")
    todo_list.append(item)
    return item

# Delete a to-do item
@app.delete("/todos/{item_id}")
def delete_todo(item_id: int):
    global todo_list
    todo_list = [item for item in todo_list if item.id != item_id]
    return {"message": f"Item {item_id} deleted"}
