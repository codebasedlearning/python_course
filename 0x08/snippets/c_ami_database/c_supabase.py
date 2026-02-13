"""
This snippet demonstrates a FastAPI + Supabase To-Do REST API,
including a standalone Supabase client example (commented out).

Teaching focus
  - Supabase client setup
  - FastAPI + Supabase integration
  - CRUD operations via Supabase

Preparations
  - .env file with SUPABASE_URL and SUPABASE_KEY, not part of the project
  - virtual environment activated and libs installed, here:
        pip install supabase fastapi uvicorn

Usage
  - Run with: uvicorn c_supabase:app --reload
  - Example curl command:
        curl -X POST http://127.0.0.1:8000/todos \\
            -H "Content-Type: application/json" \\
            -d '{"task": "Build Supabase app", "done": false}'
"""

# pip install supabase

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
import os

# Replace with your Supabase details
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://your-project.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "your-anon-key")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

class Todo(BaseModel):
    task: str
    done: bool = False

@app.get("/todos")
def get_todos():
    response = supabase.table("todos").select("*").execute()
    return response.data

@app.post("/todos")
def add_todo(todo: Todo):
    response = supabase.table("todos").insert(todo.dict()).execute()
    return response.data

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: str):
    response = supabase.table("todos").delete().eq("id", todo_id).execute()
    if not response.data:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Deleted"}

# uvicorn c_supabase:app --reload

"""
Standalone Supabase client example (without FastAPI):

from supabase import create_client, Client
from uuid import UUID

SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_todo(task: str):
    data = {"task": task, "done": False}
    response = supabase.table("todos").insert(data).execute()
    print("Added:", response.data)

def list_todos():
    response = supabase.table("todos").select("*").execute()
    for item in response.data:
        print(f"{item['id']}: {item['task']} [done: {item['done']}]")

def delete_todo(todo_id: str):
    response = supabase.table("todos").delete().eq("id", todo_id).execute()
    print("Deleted:", response.data)

if __name__ == "__main__":
    print("Current To-Dos:")
    list_todos()

    print("\\nAdding a new task...")
    add_todo("Learn how to use Supabase without FastAPI")

    print("\\nUpdated To-Dos:")
    list_todos()

    # Uncomment to delete something (replace with a real ID)
    # delete_todo("c4b0f484-47de-4894-8a8c-74cf4555e13c")
"""
