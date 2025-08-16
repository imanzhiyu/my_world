"""
FilePath: models/private_session.py
Author: Joel
Date: 2025-08-16 19:34:34
LastEditTime: 2025-08-16 19:41:01
Description: 
"""
from datetime import datetime
from models import db


class PrivateSession(db.Model):
    __tablename__ = 'private_sessions'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(128), unique=True, nullable=False)  # Flask session_id
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expired_at = db.Column(db.DateTime, nullable=False)

    def is_expired(self):
        return datetime.utcnow() > self.expired_at
