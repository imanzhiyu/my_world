"""
FilePath: routes/personal.py
Author: Joel
Date: 2025-08-12 18:09:00
LastEditTime: 2025-08-12 20:56:02
Description: 
"""
from flask import Blueprint, render_template
from models.personal import PersonalInfo

personal_bp = Blueprint('personal', __name__)


@personal_bp.route('/')
def personal_view():
    personal = PersonalInfo.query.first()
    return render_template('personal.html', personal=personal)
