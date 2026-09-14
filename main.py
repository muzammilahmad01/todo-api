from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from itertools import count

app = FastAPI(title="To-Do List API")

# In-memory storage. Resets on restart — that's fine, no DB required.
tasks: dict[int, dict] = {}
_id_counter = count(1)


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    done: bool = False


@app.post("/tasks", response_model=Task, status_code=201)
def add_task(payload: TaskCreate):
    """Create a new task."""
    task_id = next(_id_counter)
    task = {
        "id": task_id,
        "title": payload.title,
        "description": payload.description,
        "done": False,
    }
    tasks[task_id] = task
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    """Return every task currently stored."""
    return list(tasks.values())


@app.patch("/tasks/{task_id}/done", response_model=Task)
def mark_done(task_id: int):
    """Mark a specific task as done."""
    task = tasks.get(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task["done"] = True
    return task


@app.get("/")
def root():
    return {"message": "To-Do API is running. See /docs for interactive API docs."}