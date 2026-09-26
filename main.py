from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()
app = FastAPI()

# API key
API_KEY = os.getenv("API_KEY")


# -----------------------------
# Models
# -----------------------------

class Project(BaseModel):
    name: str
    language: str
    year: int


class ProjectUpdate(BaseModel):
    name: str | None = None
    language: str | None = None
    year: int | None = None


# -----------------------------
# API Key Authentication
# -----------------------------

def check_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )


# -----------------------------
# Database
# -----------------------------

def get_db():
    connection = sqlite3.connect("projects.db")
    connection.row_factory = sqlite3.Row
    return connection


def create_table():
    connection = get_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            language TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    """)

    connection.commit()
    connection.close()


create_table()


# -----------------------------
# GET - Read all projects
# -----------------------------

@app.get("/projects")
def get_projects(
    x_api_key: str = Header(...)
):
    check_api_key(x_api_key)

    connection = get_db()

    projects = connection.execute(
        "SELECT * FROM projects"
    ).fetchall()

    connection.close()

    return {
        "projects": [dict(project) for project in projects]
    }


# -----------------------------
# POST - Create project
# -----------------------------

@app.post("/projects")
def add_project(
    project: Project,
    x_api_key: str = Header(...)
):
    check_api_key(x_api_key)

    connection = get_db()

    cursor = connection.execute(
        """
        INSERT INTO projects (name, language, year)
        VALUES (?, ?, ?)
        """,
        (
            project.name,
            project.language,
            project.year
        )
    )

    connection.commit()

    project_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Project added successfully",
        "id": project_id
    }


# -----------------------------
# PUT - Replace entire project
# -----------------------------

@app.put("/projects/{project_id}")
def update_project(
    project_id: int,
    project: Project,
    x_api_key: str = Header(...)
):
    check_api_key(x_api_key)

    connection = get_db()

    existing = connection.execute(
        "SELECT * FROM projects WHERE id = ?",
        (project_id,)
    ).fetchone()

    if existing is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    connection.execute(
        """
        UPDATE projects
        SET name = ?, language = ?, year = ?
        WHERE id = ?
        """,
        (
            project.name,
            project.language,
            project.year,
            project_id
        )
    )

    connection.commit()
    connection.close()

    return {
        "message": "Project replaced successfully"
    }


# -----------------------------
# PATCH - Update selected fields
# -----------------------------

@app.patch("/projects/{project_id}")
def patch_project(
    project_id: int,
    project: ProjectUpdate,
    x_api_key: str = Header(...)
):
    check_api_key(x_api_key)

    connection = get_db()

    existing = connection.execute(
        "SELECT * FROM projects WHERE id = ?",
        (project_id,)
    ).fetchone()

    if existing is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_name = (
        project.name
        if project.name is not None
        else existing["name"]
    )

    new_language = (
        project.language
        if project.language is not None
        else existing["language"]
    )

    new_year = (
        project.year
        if project.year is not None
        else existing["year"]
    )

    connection.execute(
        """
        UPDATE projects
        SET name = ?, language = ?, year = ?
        WHERE id = ?
        """,
        (
            new_name,
            new_language,
            new_year,
            project_id
        )
    )

    connection.commit()
    connection.close()

    return {
        "message": "Project updated successfully"
    }


# -----------------------------
# DELETE - Delete project
# -----------------------------

@app.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    x_api_key: str = Header(...)
):
    check_api_key(x_api_key)

    connection = get_db()

    existing = connection.execute(
        "SELECT * FROM projects WHERE id = ?",
        (project_id,)
    ).fetchone()

    if existing is None:
        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    connection.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,)
    )

    connection.commit()
    connection.close()

    return {
        "message": "Project deleted successfully"
    }

