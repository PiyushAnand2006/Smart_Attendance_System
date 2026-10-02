# SmartAttend — Intelligent Attendance & Parent Notification System

SmartAttend is a full-stack attendance platform for colleges and training institutes.
Faculty run QR-based attendance sessions from a dashboard, students mark themselves
present by scanning the session QR (camera) or entering the session token manually,
and the system keeps attendance records, analytics, reports, and parent notifications
in one place.

## Key Features

- Role-based sign-in for Student, Faculty (Teacher), and Admin, with JWT auth.
- Faculty class scheduling with explicit Start, active-session QR display, and End Session.
- Session-scoped QR tokens that refresh every 2 minutes and remain scannable while valid.
- Student attendance via live camera scanning (`html5-qrcode`) plus manual token entry.
- Backend accepts both raw tokens (`TKN...`) and full scan URLs.
- Dashboards for Admin, Faculty, and Student, with attendance history and analytics.
- Printable reports, attendance calculator, and WhatsApp-style parent notification queue.
- SQLite + SQLAlchemy backend with idempotent demo-data seeding.

## Tech Stack

| Layer    | Technology |
|----------|------------|
| Backend  | Flask, Flask-CORS, PyJWT, SQLAlchemy, SQLite |
| Frontend | Next.js 14, React 18, TypeScript, Tailwind CSS |
| QR       | `qrcode.react` for display, `html5-qrcode` for camera scanning |
| Auth     | Email/password login, JWT access token in `localStorage` |

## How It Works

### Roles

| Role    | Portal Prefix | Typical Use |
|---------|---------------|-------------|
| Admin   | `/admin`      | Manage students, faculty, classes, reports, settings |
| Faculty | `/faculty`    | Schedule classes, run QR sessions, view history and reports |
| Student | `/student`    | Scan QR or enter token, view subjects, history, calculator, reports |

The login page offers Student, Admin, and Teacher buttons that pre-fill demo
credentials and send the selected role to the backend for validation.

### Attendance Flow

1. Faculty creates a class from Schedule with subject, class, mode, and date.
2. Faculty clicks Start on a scheduled class and opens its QR page.
3. Opening the QR page activates the session and generates a backend-backed token.
4. Students scan the QR with their camera or paste the displayed token manually.
5. Session stats update live; faculty ends the session when attendance is complete.

## Repository Structure

```text
backend/         - Flask API: app/, run.py, app_minimal.py, requirements.txt
frontend/        - Next.js UI: src/app for admin, faculty, student portals
docs/            - Additional documentation
tests/           - API tests
scripts/         - Helper scripts
start.py         - Chooses minimal or full backend for local runs
QUICKSTART.md    - Short setup guide
RUN.md           - Detailed run, stop, and troubleshooting guide
```

## Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- A webcam for camera-based QR scanning

## Getting Started

### 1. Install dependencies

```bash
pip install -r backend/requirements.txt
cd frontend
npm install
```

### 2. Start the backend

```bash
cd backend
python run.py
```

The API runs at `http://localhost:5000`, with health at `http://localhost:5000/health`.

Alternatively, `python start.py` from the repository root lets you choose between the
full structured backend and the minimal single-file backend.

### 3. Start the frontend

```bash
cd frontend
npm run dev
```

The UI runs at `http://localhost:3000` and proxies `/api/*` to the backend on port 5000.

### 4. Demo Accounts

| Role    | Email                    | Password   |
|---------|--------------------------|------------|
| Admin   | `admin@smartattend.com`   | `admin123` |
| Faculty | `faculty@smartattend.com` | `faculty123` |
| Student | `student@smartattend.com` | `student123` |

Tip: test faculty and student flows in separate browsers or incognito windows.
Auth tokens are stored in `localStorage`, which is shared across tabs in the same
browser, so logging in as another role in one tab replaces the token used by other tabs.

## API Reference

| Method | Endpoint                              | Access          | Purpose |
|--------|---------------------------------------|-----------------|---------|
| POST   | `/api/auth/login`                     | Public          | Login with email, password, and role |
| POST   | `/api/auth/register`                  | Public          | Register a student or faculty account |
| GET    | `/api/auth/me`                        | Authenticated   | Current user profile |
| GET    | `/api/attendance/sessions`            | Faculty, Admin  | List attendance sessions |
| POST   | `/api/attendance/sessions`            | Faculty, Admin  | Create an attendance session |
| GET    | `/api/attendance/sessions/<id>`       | All roles       | Session details, records, and counts |
| POST   | `/api/attendance/sessions/<id>/start` | Faculty, Admin  | Mark a scheduled session active |
| POST   | `/api/attendance/sessions/<id>/end`   | Faculty, Admin  | Complete a session |
| POST   | `/api/qr/generate`                    | Faculty, Admin  | Generate a token for a session |
| POST   | `/api/qr/scan-my`                     | Student         | Mark own attendance with a token |
| POST   | `/api/qr/scan`                        | All roles       | Mark attendance with token and student ID |
| GET    | `/api/attendance/my-attendance`       | Student         | Student's attendance records |

Run the API checks with:

```bash
cd tests
python test_api.py
```

## Configuration

Backend QR token lifetime is configured through `QR_TOKEN_EXPIRY_SECONDS`
in `backend/config/__init__.py`, defaulting to 300 seconds. The faculty QR display
refreshes every 120 seconds, so tokens intentionally remain valid longer than the
display interval.

## Troubleshooting

- Page loads without styling: restart the Next.js dev server; a production build can conflict with it.
- Port already in use: stop the process on ports 3000 or 5000, then restart that service.
- `Access denied` on faculty pages: re-login as faculty; another tab may have replaced the shared auth token with a student login.
- `Invalid or expired QR code`: use a freshly generated token from an active session; both raw tokens and full scan URLs are accepted.
- Camera unavailable: grant browser camera permission, preferably test on HTTPS or localhost.

## License

MIT
