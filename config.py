"""
FilePath: config.py
Author: Joel
Date: 2025-08-10 09:44:57
LastEditTime: 2025-08-14 15:39:58
Description: 配置
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, 'db')
if not os.path.exists(db_path):
    os.makedirs(db_path)

# print(db_path)
from dotenv import load_dotenv
import secrets

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_hex(16)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{db_path}\site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True  # 防止 SSL connection closed
    }
