"""
FilePath: models/personal.py
Author: Joel
Date: 2025-08-11 22:03:26
LastEditTime: 2025-08-14 15:53:05
Description: 
"""
from datetime import datetime
from models import db
import json


class PersonalInfo(db.Model):
    __tablename__ = 'personal_info'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)  # 用户头像
    location = db.Column(db.String(120), nullable=True)  # 所在城市
    links = db.Column(db.Text, nullable=True)  # 存 JSON
    skills = db.Column(db.Text, nullable=True)  # 技能，逗号分隔
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_links(self):
        """解析 JSON 成 Python 列表"""
        if self.links:
            try:
                return json.loads(self.links)
            except json.JSONDecodeError:
                return []
        return []

    def set_links(self, links_list):
        """将 Python 列表存成 JSON"""
        self.links = json.dumps(links_list, ensure_ascii=False)

    def __repr__(self):
        return f'<PersonalInfo {self.name}>'
