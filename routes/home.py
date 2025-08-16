"""
FilePath: routes/home.py
Author: Joel
Date: 2025-08-10 09:47:39
LastEditTime: 2025-08-16 19:59:15
Description: 
"""
import os
from flask import Blueprint, render_template, current_app, send_from_directory, request

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    cards = [
        {"title": "Tools", "desc": "一些免费小程序供下载", "img": "cards/tools_bg.jpg", "link": "/tools"},
        {"title": "Blogs", "desc": "我的文章与分享", "img": "cards/blog_bg.jpg", "link": "/blog"},
        {"title": "Research", "desc": "科研资源与分享", "img": "cards/research_bg.jpg", "link": "/research"},
        # {"title": "学术研究", "desc": "科研资源与分享", "img": "cards/research_bg.jpg", "link": "#"},
        # {"title": "Private", "desc": "需要密码才能访问", "img": "cards/private_bg.jpg", "link": "/private"},
        # {"title": "关于我", "desc": "个人简介", "img": "cards/about_bg.jpg", "link": "#"}
    ]
    return render_template('home.html', cards=cards)


# 上传的工具
@home_bp.route('/uploads/<path:filename>')
def uploaded_files(filename):
    upload_dir = os.path.join(current_app.instance_path, 'uploads')
    return send_from_directory(upload_dir, filename)


# ping 健康检查接口
@home_bp.route('/ping')
def ping():
    secret = request.args.get('key')
    if secret != 'Wyyrwcyx2589.':
        return "Unauthorized", 403
    return "pong", 200


from datetime import datetime
from models.private_session import PrivateSession
from flask import jsonify
from models import db


@home_bp.route('/private/sessions/cleanup', methods=['GET', 'POST'])
def cleanup_expired_sessions():
    try:
        secret = request.args.get('key')
        if secret != 'Wyyrwcyx2589.':
            return "Unauthorized", 403

        now = datetime.utcnow()
        deleted_count = PrivateSession.query.filter(PrivateSession.expired_at < now).delete()
        db.session.commit()
        return jsonify({'success': True, 'deleted': deleted_count})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
