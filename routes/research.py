"""
FilePath: routes/research.py
Author: Joel
Date: 2025-08-12 18:07:51
LastEditTime: 2025-08-13 18:35:55
Description: 
"""
from flask import Blueprint, render_template
from models.research import ResearchContent

research_bp = Blueprint('research', __name__)


@research_bp.route('/')
def research_list():
    contents = ResearchContent.query.order_by(ResearchContent.created_at.desc()).all()
    return render_template('research.html', contents=contents)


@research_bp.route('/<int:content_id>')
def research_detail(content_id):
    content = ResearchContent.query.get_or_404(content_id)
    return render_template('research_detail.html', content=content)
