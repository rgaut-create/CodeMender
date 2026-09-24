"""
Vulnerable Flask Web Application for CodeMender CI/CD Security Scanning Demo.
Contains SQL Injection, IDOR, and Command Injection vulnerabilities.
"""

import os
import sqlite3
from flask import Flask, request, jsonify, g

app = Flask(__name__)
DATABASE = 'demo_app.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        db.commit()

        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO users (username, email, role) VALUES ('admin', 'admin@example.com', 'admin')")
            cursor.execute("INSERT INTO users (username, email, role) VALUES ('alice', 'alice@example.com', 'user')")
            cursor.execute("INSERT INTO users (username, email, role) VALUES ('bob', 'bob@example.com', 'user')")
            
            cursor.execute("INSERT INTO documents (owner_id, title, content) VALUES (1, 'Admin Confidential', 'Super Secret Admin Report')")
            cursor.execute("INSERT INTO documents (owner_id, title, content) VALUES (2, 'Alice Notes', 'Alice Private Journal')")
            cursor.execute("INSERT INTO documents (owner_id, title, content) VALUES (3, 'Bob Notes', 'Bob Public Work')")
            db.commit()


# ------------------------------------------------------------------------------
# VULNERABILITY 1: SQL Injection (SQLi)
# ------------------------------------------------------------------------------
@app.route('/api/user/search', methods=['GET'])
def search_user():
    username = request.args.get('username', '')
    db = get_db()
    cursor = db.cursor()
    
    # VULNERABLE: Direct string formatting into SQL query
    query = f"SELECT id, username, email, role FROM users WHERE username = '{username}'"
    try:
        cursor.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
        return jsonify({"status": "success", "data": results})
    except sqlite3.Error as e:
        return jsonify({"status": "error", "message": str(e)}), 400


# ------------------------------------------------------------------------------
# VULNERABILITY 2: Insecure Direct Object Reference (IDOR)
# ------------------------------------------------------------------------------
@app.route('/api/documents/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    current_user_id = request.headers.get('X-User-ID')
    if not current_user_id:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    db = get_db()
    cursor = db.cursor()
    
    # VULNERABLE: Fetches document solely by doc_id without checking owner_id
    cursor.execute("SELECT id, owner_id, title, content FROM documents WHERE id = ?", (doc_id,))
    doc = cursor.fetchone()
    
    if not doc:
        return jsonify({"status": "error", "message": "Document not found"}), 404
        
    return jsonify({"status": "success", "data": dict(doc)})


# ------------------------------------------------------------------------------
# VULNERABILITY 3: Command Injection (RCE)
# ------------------------------------------------------------------------------
@app.route('/api/tools/ping', methods=['POST'])
def ping_host():
    data = request.get_json() or {}
    host = data.get('host', '')
    
    if not host:
        return jsonify({"status": "error", "message": "Host is required"}), 400
        
    # VULNERABLE: Direct execution of user input in shell command
    command = f"ping -c 1 {host}"
    exit_code = os.system(command)
    
    if exit_code == 0:
        return jsonify({"status": "success", "message": f"Host {host} is reachable"})
    else:
        return jsonify({"status": "error", "message": f"Failed to ping {host}"}), 500


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
