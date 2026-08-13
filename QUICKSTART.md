# SmartAttend

Intelligent Multi-Modal Attendance & Parent Notification System

## Quick Start

### 1. Install backend dependencies

```bash
pip install -r backend/requirements.txt
# i.e. Flask, flask-cors, PyJWT
```

### 2. Start the Backend (choose one)

```bash
# Full backend (structured Flask + JWT, all endpoints)
cd backend
python run.py

# ...or the minimal single-file backend
python app_minimal.py
```

API runs at http://localhost:5000

### 3. Demo Credentials

- Admin: `admin@smartattend.com` / `admin123`
- Faculty: `faculty@smartattend.com` / `faculty123`
- Student: `student@smartattend.com` / `student123`

### 4. Test the API

```bash
cd tests
python test_api.py
```

Or manually:

```bash
curl http://localhost:5000/health

curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@smartattend.com","password":"admin123"}'
```

### 5. Run the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at http://localhost:3000 and proxies `/api/*` to the backend on port 5000.

## Features

- Multi-Modal Attendance (Face + QR)
- WhatsApp Parent Notifications (Mock queue + templates)
- Three Dashboards (Admin/Faculty/Student)
- Attendance Analytics & Risk Prediction
- Printable Monthly Reports
- Attendance Calculator
- Student Registration

## Architecture

- Backend: Flask + PyJWT (structured, `backend/app/`) or in-memory minimal (`backend/app_minimal.py`)
- Frontend: Next.js 14 + React + TypeScript + Tailwind CSS
- Theme: "Midnight Academic Intelligence"

## Project Structure

```
backend/         - Flask API (app/, run.py, app_minimal.py)
frontend/        - Next.js UI
docs/            - Documentation
tests/           - API tests
```

## License

MIT
