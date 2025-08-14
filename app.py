"""
FilePath: app.py
Author: Joel
Date: 2025-08-10 09:41:06
LastEditTime: 2025-08-12 18:11:31
Description: main
"""
import os
from flask import Flask
from routes.home import home_bp
from routes.tools import tools_bp
from routes.blog import blog_bp
from routes.private import private_bp
from routes.english import english_bp
from routes.personal import personal_bp
from routes.research import research_bp
from models import db


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # 初始化数据库
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # 注册蓝图
    app.register_blueprint(home_bp)
    app.register_blueprint(tools_bp, url_prefix='/tools')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(english_bp, url_prefix='/english')
    app.register_blueprint(research_bp, url_prefix='/research')
    app.register_blueprint(personal_bp, url_prefix='/personal')
    app.register_blueprint(private_bp, url_prefix='/private')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
