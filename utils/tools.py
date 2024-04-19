import os
from datetime import datetime, timezone
from flask import jsonify
from db import users
from db import db_connect as dbc


# FILENAMES
LOG_FILE = 'access_logs.txt'
ADMIN_LOG_FILE = 'admin_access_logs.txt'


def verify_identity(user):
    email = user[users.EMAIL]
    password = user[users.PASSWORD]

    if not email:
        raise ValueError('Email may not be blank')
    if not password:
        raise ValueError('Password may not be blank')
    dbc.connect_db()
    data = dbc.fetch_one(users.USERS_COLLECT, {users.EMAIL: email})
    if not data:
        raise ValueError('Invalid email or password')
    if not users.verify_password(password, data[users.PASSWORD]):
        raise ValueError('Invalid email or password')
    if users.IS_ADMIN not in data or not data[users.IS_ADMIN]:
        raise ValueError('Not an admin')
    return True


def log_access(endpoint, request, isAdmin=False):
    log_file_name = LOG_FILE
    if isAdmin:
        log_file_name = ADMIN_LOG_FILE

    # CREATE "ACCESS_LOG" FILE IF NOT FOUND
    if not os.path.exists(log_file_name):
        open(log_file_name, 'w').close()

    log_entry = {
        'endpoint': endpoint,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'ip_address': request.remote_addr  # Add this line
    }

    with open(log_file_name, 'a') as log_file:
        log_file.write(f"{log_entry}\n")

def get_access_logs_in_str(isAdmin=False):
    log_file_name = LOG_FILE
    if isAdmin:
        log_file_name = ADMIN_LOG_FILE

    if not os.path.exists(LOG_FILE):
        return { "message": "Access logs file not found" }
    
    access_logs = []
    with open(log_file_name, 'r') as log_file:
        for line in log_file:
            try:
                log_entry = eval(line)  # Convert string to dictionary
                access_logs.append(log_entry)
            except (ValueError, SyntaxError):
                # Skip any invalid log entries
                continue
    return jsonify(access_logs)