"""
FilePath: models/research.py
Author: Joel
Date: 2025-08-11 22:17:34
LastEditTime: 2025-08-13 18:47:20
Description: 
"""
from datetime import datetime
from models import db


class ResearchContent(db.Model):
    __tablename__ = 'research_content'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), default="")
    description = db.Column(db.Text, default="")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ResearchContent id={self.id} title={self.title}>"
