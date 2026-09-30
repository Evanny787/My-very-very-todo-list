# Todo app (FastAPI + React + SQLite)

    todo-app/
      todo-backend/    Python + FastAPI + SQLite  (main.py, requirements.txt)
      todo-frontend/   React (Vite)               (package.json, src/App.jsx)

You need Python 3.10+ and Node.js 18+. Use two terminals.

**Terminal 1 - backend**
    cd todo-backend
    pip install -r requirements.txt
    uvicorn main:app --reload
Runs on http://localhost:8000 and creates todos.db automatically.

**Terminal 2 - frontend**
    cd todo-frontend
    npm install
    npm run dev
Open http://localhost:5173.

## Deploying (backend and frontend are deployed separately)
- Backend: root directory `todo-backend`, install `pip install -r requirements.txt`,
  start `uvicorn main:app --host 0.0.0.0 --port $PORT`.
  Set `ALLOWED_ORIGINS` to your frontend's web address.
- Frontend: root directory `todo-frontend`, build `npm run build`, output `dist`.
  Set `VITE_API_URL` to your backend's web address.
- Note: many hosts wipe the disk on restart, which would erase the SQLite file.
