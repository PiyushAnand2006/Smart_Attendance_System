# SmartAttend — How to Run

Run the whole project (Flask backend + Next.js frontend) with minimal effort.

---

## Prerequisites

| Tool        | Version      | Check            |
|-------------|--------------|------------------|
| Python      | 3.10+        | `python --version` |
| Node.js     | 18+          | `node --version`   |
| npm         | any recent   | `npm --version`    |

---

## 1. Install dependencies (first time only)

```bash
pip install -r backend/requirements.txt
cd frontend && npm install
```

---

## 2. Run in a single stroke

Copy-paste **one** of the commands below, depending on your shell.

### Git Bash (Windows) / macOS / Linux

```bash
(cd backend && python run.py) & (cd frontend && npm run dev)
```

### Windows PowerShell

```powershell
Start-Process python -ArgumentList 'run.py' -WorkingDirectory 'backend'; Set-Location frontend; npm run dev
```

### Windows Command Prompt (CMD)

```cmd
start cmd /k "cd backend && python run.py" && cd frontend && npm run dev
```

> **Note:** The first frontend start can take ~10–20 s to compile. Give it a moment.

---

## 3. Run manually (two terminals — easier for debugging)

**Terminal 1 — Backend (Flask API):**

```bash
cd backend
python run.py
```

**Terminal 2 — Frontend (Next.js UI):**

```bash
cd frontend
npm run dev
```

---

## URLs

| Service  | URL                                |
|----------|------------------------------------|
| Frontend | http://localhost:3000              |
| Backend  | http://localhost:5000              |
| Health   | http://localhost:5000/health       |

The frontend automatically proxies `/api/*` requests to the backend on port 5000.

---

## Demo credentials

| Role    | Email                        | Password  |
|---------|------------------------------|-----------|
| Admin   | `admin@smartattend.com`      | `admin123` |
| Faculty | `faculty@smartattend.com`    | `faculty123` |
| Student | `student@smartattend.com`    | `student123` |

---

## Stop the servers

- **Manual terminals:** press `Ctrl+C` in each terminal.
- **Single-stroke Git Bash:** press `Ctrl+C` (then, if the backend lingers, kill it — see below).

---

## If a port is already in use (stuck server)

Find and kill whatever holds the port:

**Windows (PowerShell or CMD):**

```bash
netstat -ano | findstr :5000     # note the PID (last column)
taskkill /PID <PID> /F
```

```bash
netstat -ano | findstr :3000     # note the PID (last column)
taskkill /PID <PID> /F
```

**Git Bash / macOS / Linux:**

```bash
lsof -i :5000 -i :3000           # find the PIDs
kill -9 <PID>
```

Then re-run the start command above.

---

## Troubleshooting

- **`ModuleNotFoundError: flask`** → run the backend install step again.
- **`npm: command not found`** → install Node.js/npm first.
- **Frontend loads but API calls fail** → confirm the backend is running (`curl http://localhost:5000/health` should return `{"service": "SmartAttend API", "status": "healthy"}`).
- **Port already in use** → follow the "port in use" section above.
