"""
Unit tests for Flask Vulnerable Demo App.
Verifies functional requirements and test suite compatibility.
"""

import pytest
import os
import sqlite3
from app import app, init_db, DATABASE

@pytest.fixture
def client():
    app.config['TESTING'] = True
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        
    init_db()
    with app.test_client() as client:
        yield client
        
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

def test_user_search_valid(client):
    response = client.get('/api/user/search?username=alice')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert len(data['data']) == 1
    assert data['data'][0]['username'] == 'alice'

def test_get_document_authorized(client):
    response = client.get('/api/documents/2', headers={'X-User-ID': '2'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['data']['title'] == 'Alice Notes'

def test_ping_host_localhost(client):
    response = client.post('/api/tools/ping', json={'host': '127.0.0.1'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
