"""
FilePath: models/__init__.py
Author: Joel
Date: 2025-08-10 09:46:23
LastEditTime: 2025-08-10 16:42:38
Description: 
"""
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from models.blog import Blog
