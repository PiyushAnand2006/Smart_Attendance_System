"""Minimal SmartAttend Backend"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid, hashlib, secrets
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
CORS(app)

db = {'users': [], 'students': [], 'faculty': [], 'parents': [],
      'classes': [], 'subjects': [], 'attendance_sessions': [],
      'attendance_records': [], 'qr_identities': [],
      'notification_templates': [], 'notification_queue': []}
tokens = {}

def hash_pwd(p):
    return hashlib.sha256(p.encode()).hexdigest()

def gen_token(uid, role):
    t = secrets.token_urlsafe(32)
    tokens[t] = {'user_id': uid, 'role': role, 'expires': datetime.utcnow() + timedelta(hours=24)}
    return t

def auth_required(f):
    @wraps(f)
    def dec(*a, **kw):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if token not in tokens:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        return f(*a, **kw)
    return dec

def role_required(*roles):
    def dec(f):
        @wraps(f)
        def wrapper(*a, **kw):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if token not in tokens:
                return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
            if tokens[token]['role'] not in roles:
                return jsonify({'status': 'error', 'message': 'Forbidden'}), 403
            return f(*a, **kw)
        return wrapper
    return dec

def init_demo():
    if db['users']:
        return
    db['users'].append({'id': 1, 'user_id': 'ADM001', 'email': 'admin@smartattend.com', 'password': hash_pwd('admin123'), 'role': 'admin', 'is_active': True})
    db['users'].append({'id': 2, 'user_id': 'FAC001', 'email': 'faculty@smartattend.com', 'password': hash_pwd('faculty123'), 'role': 'faculty', 'is_active': True})
    db['users'].append({'id': 3, 'user_id': 'STU001', 'email': 'student@smartattend.com', 'password': hash_pwd('student123'), 'role': 'student', 'is_active': True})
    db['faculty'].append({'id': 1, 'faculty_id': 'FAC1001', 'user_id': 2, 'first_name': 'Dr. Rajesh', 'last_name': 'Kumar', 'department': 'Computer Science'})
    db['classes'].append({'id': 1, 'name': 'Computer Science', 'code': 'CSE', 'department': 'Engineering'})
    for s in [{'name': 'Database Management Systems', 'code': 'DBMS'}, {'name': 'Artificial Intelligence', 'code': 'AI'}, {'name': 'Operating Systems', 'code': 'OS'}, {'name': 'Computer Networks', 'code': 'CN'}]:
        db['subjects'].append({'id': len(db['subjects']) + 1, **s, 'credits': 3, 'department': 'CSE', 'semester': 1, 'is_active': True})
    names = [('Rahul', 'Sharma'), ('Priya', 'Patil'), ('Amit', 'Kumar'), ('Sneha', 'Rao'), ('Vikram', 'Singh'), ('Ananya', 'Gupta'), ('Ravi', 'Reddy'), ('Kavya', 'Nair'), ('Arjun', 'Menon'), ('Divya', 'Iyer'), ('Suresh', 'Naidu'), ('Meera', 'Das'), ('Nikhil', 'Verma'), ('Pooja', 'Shetty'), ('Kiran', 'Bhat')]
    for i, (f, l) in enumerate(names, 1):
        db['students'].append({'id': i, 'student_id': f'STU{i:04d}', 'first_name': f, 'last_name': l, 'roll_number': f'42{i:02d}', 'class_id': 1, 'section': 'A', 'department': 'CSE', 'enrollment_status': 'ready' if i == 1 else 'incomplete', 'is_active': True})
        db['parents'].append({'id': i, 'student_id': i, 'name': f'Mr. {l}', 'whatsapp_number': f'+9198765{i:05d}', 'relationship': 'father'})
        db['qr_identities'].append({'id': i, 'student_id': i, 'qr_identifier': f'QR{uuid.uuid4().hex[:8].upper()}', 'is_active': True})
    for t in [{'name': 'present', 'display_name': 'Present', 'content': 'Dear {{parent_name}}, {{student_name}} attendance recorded.'}, {'name': 'late', 'display_name': 'Late', 'content': 'Dear {{parent_name}}, {{student_name}} arrived late.'}, {'name': 'absent', 'display_name': 'Absent', 'content': 'Dear {{parent_name}}, {{student_name}} was absent.'}, {'name': 'warning', 'display_name': 'Warning', 'content': 'Dear {{parent_name}}, attendance low.'}]:
        db['notification_templates'].append({'id': len(db['notification_templates']) + 1, **t, 'is_active': True})

init_demo()
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'SmartAttend API'})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = next((u for u in db['users'] if u['email'] == data.get('email')), None)
    if not user or hash_pwd(data.get('password', '')) != user['password']:
        return jsonify({'status': 'error', 'message': 'Invalid'}), 401
    token = gen_token(user['user_id'], user['role'])
    return jsonify({'status': 'success', 'data': {'access_token': token, 'user': {k: v for k, v in user.items() if k != 'password'}, 'role': user['role']}})

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    if any(u['email'] == data.get('email') for u in db['users']):
        return jsonify({'status': 'error', 'message': 'Email exists'}), 400
    user = {'id': len(db['users']) + 1, 'user_id': f'USR{uuid.uuid4().hex[:8].upper()}', 'email': data['email'], 'password': hash_pwd(data['password']), 'role': data.get('role', 'student'), 'is_active': True}
    db['users'].append(user)
    return jsonify({'status': 'success', 'data': {'access_token': gen_token(user['user_id'], user['role']), 'user': {k: v for k, v in user.items() if k != 'password'}, 'role': user['role']}}), 201

@app.route('/api/students', methods=['GET'])
@auth_required
def get_students():
    return jsonify({'status': 'success', 'data': db['students'], 'meta': {'total': len(db['students'])}})

@app.route('/api/students/<int:sid>', methods=['GET'])
@auth_required
def get_student(sid):
    s = next((x for x in db['students'] if x['id'] == sid), None)
    if not s:
        return jsonify({'status': 'error', 'message': 'Not found'}), 404
    return jsonify({'status': 'success', 'data': {**s, 'full_name': f"{s['first_name']} {s['last_name']}", 'overall_attendance': 84.5}})

@app.route('/api/admin/dashboard', methods=['GET'])
@role_required('admin')
def admin_dash():
    return jsonify({'status': 'success', 'data': {'total_students': len(db['students']), 'total_faculty': len(db['faculty']), 'total_classes': len(db['classes']), 'avg_attendance': 84.6, 'whatsapp_sent': 11, 'whatsapp_failed': 0}})

@app.route('/api/faculty/dashboard', methods=['GET'])
@role_required('faculty', 'admin')
def fac_dash():
    return jsonify({'status': 'success', 'data': {'today_sessions': [{'id': 1, 'subject_name': 'Database Management Systems', 'class_name': 'CSE-A', 'time': '09:00 AM', 'status': 'active'}], 'today_total': 15, 'today_present': 11, 'attendance_rate': 73.3}})

@app.route('/api/attendance/sessions', methods=['POST'])
@role_required('faculty', 'admin')
def create_session():
    data = request.json
    s = {'id': len(db['attendance_sessions']) + 1, 'session_id': f'SES{uuid.uuid4().hex[:8].upper()}', 'subject_id': data.get('subject_id', 1), 'class_id': data.get('class_id', 1), 'faculty_id': 1, 'attendance_mode': data.get('mode', 'FACE'), 'status': 'active', 'total_students': 15}
    db['attendance_sessions'].append(s)
    return jsonify({'status': 'success', 'data': s}), 201

@app.route('/api/attendance/sessions/<int:sid>/mark', methods=['POST'])
@role_required('faculty', 'admin')
def mark_att(sid):
    data = request.json
    student_id = data.get('student_id')
    if any(r['student_id'] == student_id and r['session_id'] == sid for r in db['attendance_records']):
        return jsonify({'status': 'error', 'message': 'Duplicate'}), 400
    rec = {'id': len(db['attendance_records']) + 1, 'student_id': student_id, 'session_id': sid, 'status': 'PRESENT', 'attendance_method': data.get('method', 'FACE')}
    db['attendance_records'].append(rec)
    student = next((s for s in db['students'] if s['id'] == student_id), None)
    if student:
        parent = next((p for p in db['parents'] if p['student_id'] == student_id), None)
        if parent:
            n = {'id': len(db['notification_queue']) + 1, 'recipient_number': parent['whatsapp_number'], 'message': f"Attendance marked for {student['first_name']}", 'status': 'SENT'}
            db['notification_queue'].append(n)
    return jsonify({'status': 'success', 'data': rec}), 201

@app.route('/api/notifications/templates', methods=['GET'])
@auth_required
def get_templates():
    return jsonify({'status': 'success', 'data': db['notification_templates']})

@app.route('/api/notifications/queue', methods=['GET'])
@role_required('admin')
def get_queue():
    return jsonify({'status': 'success', 'data': db['notification_queue'][-20:]})

@app.route('/api/reports/monthly', methods=['GET'])
@auth_required
def monthly_report():
    return jsonify({'status': 'success', 'data': {'student_name': 'Rahul Sharma', 'summary': {'percentage': 84.5}, 'subjects': [{'code': 'DBMS', 'percentage': 92}, {'code': 'AI', 'percentage': 86}]}})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    print(f"\nSmartAttend API on port {port}")
    print("Admin: admin@smartattend.com / admin123")
    print("Faculty: faculty@smartattend.com / faculty123")
    print("Student: student@smartattend.com / student123\n")
    app.run(host='0.0.0.0', port=port, debug=True)