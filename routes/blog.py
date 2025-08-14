"""
FilePath: routes/blog.py
Author: Joel
Date: 2025-08-10 09:48:00
LastEditTime: 2025-08-13 20:52:37
Description: 
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.blog import Blog
from models import db

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def blog_list():
    contents = Blog.query.order_by(Blog.created_at.desc()).all()
    return render_template('blog.html', contents=contents)


@blog_bp.route('/<int:content_id>')
def blog_detail(content_id):
    content = Blog.query.get_or_404(content_id)
    return render_template('blog_detail.html', content=content)
