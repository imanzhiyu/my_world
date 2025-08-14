"""
FilePath: models/blog.py
Author: Joel
Date: 2025-08-10 11:28:43
LastEditTime: 2025-08-13 22:21:21
Description: 
"""

from models import db
from datetime import datetime


class Blog(db.Model):
    __tablename__ = 'blog'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    cover_img = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
