"""
FilePath: routes/english.py
Author: Joel
Date: 2025-08-10 16:21:36
LastEditTime: 2025-08-13 16:44:23
Description: 
"""

from flask import Blueprint, render_template
from models.english import EnglishContent

english_bp = Blueprint('english', __name__)


@english_bp.route('/')
def english_list():
    # 查询最新一条 EnglishContent，或者全部，自己根据需求改
    contents = EnglishContent.query.order_by(EnglishContent.created_at.desc()).all()
    return render_template('english.html', contents=contents)


@english_bp.route('/<int:content_id>')
def english_detail(content_id):
    content = EnglishContent.query.get_or_404(content_id)
    return render_template('english_detail.html', content=content)
