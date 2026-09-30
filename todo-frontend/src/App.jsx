import { useEffect, useState } from "react";

// Where the backend lives. Set VITE_API_URL when you deploy.
const API = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");

  // Helper: call the backend; every endpoint returns the full, up-to-date list
  async function call(path, method = "GET", body) {
    const res = await fetch(API + path, {
      method,
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined,
    });
    setTodos(await res.json());
  }

  useEffect(() => { call("/todos"); }, []);

  function add(e) {
    e.preventDefault();
    if (!title.trim()) return;
    call("/todos", "POST", { title });
    setTitle("");
  }

  function move(index, step) {
    const ids = todos.map((t) => t.id);
    const target = index + step;
    if (target < 0 || target >= ids.length) return;
    [ids[index], ids[target]] = [ids[target], ids[index]];
    call("/todos/order", "PUT", { ids });
  }

  return (
    <div className="app">
      <h1>Todo List</h1>
      <form onSubmit={add}>
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="What needs doing?" />
        <button>Add</button>
      </form>
      <ul>
        {todos.map((t, i) => (
          <li key={t.id} className={t.done ? "done" : ""}>
            <input type="checkbox" checked={t.done} onChange={() => call(`/todos/${t.id}`, "PATCH", { done: !t.done })} />
            <span>{t.title}</span>
            <button onClick={() => move(i, -1)} disabled={i === 0}>↑</button>
            <button onClick={() => move(i, 1)} disabled={i === todos.length - 1}>↓</button>
            <button onClick={() => call(`/todos/${t.id}`, "DELETE")}>✕</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
