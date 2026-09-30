import os
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
# Which websites may call this backend. Set ALLOWED_ORIGINS when you deploy.
app.add_middleware(CORSMiddleware, allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(","),
                   allow_methods=["*"], allow_headers=["*"])

# On Vercel only the /tmp folder is writable (and it is wiped regularly)
DB_FILE = "/tmp/todos.db" if os.getenv("VERCEL") else "todos.db"

def db():
    con = sqlite3.connect(DB_FILE)
    con.row_factory = sqlite3.Row
    return con

with db() as con:
    con.execute("""CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done INTEGER NOT NULL DEFAULT 0,
        position INTEGER NOT NULL)""")

class NewTodo(BaseModel):
    title: str

class Update(BaseModel):
    done: bool

class Order(BaseModel):
    ids: list[int]

def all_todos(con):
    return [dict(r, done=bool(r["done"])) for r in con.execute("SELECT * FROM todos ORDER BY position")]

@app.get("/todos")
def list_todos():
    with db() as con:
        return all_todos(con)

@app.post("/todos")
def add_todo(body: NewTodo):
    with db() as con:
        pos = con.execute("SELECT COALESCE(MAX(position), 0) + 1 FROM todos").fetchone()[0]
        con.execute("INSERT INTO todos (title, position) VALUES (?, ?)", (body.title.strip(), pos))
        return all_todos(con)

@app.patch("/todos/{todo_id}")
def check_todo(todo_id: int, body: Update):
    with db() as con:
        con.execute("UPDATE todos SET done = ? WHERE id = ?", (int(body.done), todo_id))
        return all_todos(con)

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with db() as con:
        con.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        return all_todos(con)

@app.put("/todos/order")
def reorder(body: Order):
    with db() as con:
        for pos, todo_id in enumerate(body.ids):
            con.execute("UPDATE todos SET position = ? WHERE id = ?", (pos, todo_id))
        return all_todos(con)
