# To-Do List API

A simple in-memory to-do list REST API built with FastAPI, containerized with Docker, and built automatically via GitHub Actions on every push.

## Features

- Add a task
- List all tasks
- Mark a task as done
- In-memory storage (no database required, resets on restart)

## Running Locally (without Docker)

Requires Python 3.9 or later.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. Interactive API docs (Swagger UI) are auto-generated at `http://127.0.0.1:8000/docs`.

## Running with Docker

```bash
docker build -t todo-api .
docker run -p 8000:8000 todo-api
```

Same endpoints, same docs, running inside a container.

## API Endpoints

### `POST /tasks`
Creates a new task.

Request body:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

Response: the created task, including its assigned `id` and `done: false`.

### `GET /tasks`
Returns a list of all tasks currently stored, including their `id`, `title`, `description`, and `done` status.

### `PATCH /tasks/{task_id}/done`
Marks the task with the given `task_id` as done. Returns the updated task, or a 404 error if no task with that ID exists.

## CI/CD

A GitHub Actions workflow (`.github/workflows/docker-build.yml`) automatically builds the Docker image on every push to `main` and on every pull request targeting `main`. It confirms the image builds successfully; it does not deploy or push the image anywhere.

## Reflection

The trickiest part of this challenge was not the API code itself, it was the local environment setup. My machine had two separate Python installations (an older Apple Command Line Tools Python and a newer Homebrew Python), and they did not share installed packages. This caused `uvicorn` and `pip` commands to fail intermittently depending on which Python my shell happened to resolve to at that moment. I also ran into a bug where the newer Python's `ensurepip` failed due to a version-parsing issue during virtual environment setup.

I chose to isolate the project inside a Python virtual environment (`venv`) rather than installing dependencies globally. This keeps the project's dependencies self-contained and avoids exactly the kind of version conflict I ran into, and it means anyone cloning this repo gets a clean, reproducible setup regardless of what else is installed on their machine.

For the API itself, I chose FastAPI over alternatives like Flask because it gives built-in request validation and automatically generates interactive documentation, which made it easy to manually verify each endpoint worked correctly without writing a separate test client.

If I had another day, I would add automated tests (using `pytest` and FastAPI's `TestClient`) rather than relying on manual verification through the Swagger UI, and I would extend the GitHub Actions workflow to also run those tests before building the Docker image, so that a broken endpoint would fail CI even if the Docker build itself succeeded.