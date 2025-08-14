"""
FilePath: routes/tools.py
Author: Joel
Date: 2025-08-10 09:47:50
LastEditTime: 2025-08-13 10:50:55
Description: 
"""

import os
import glob
from flask import Blueprint, render_template, current_app, send_from_directory

tools_bp = Blueprint('tools', __name__)


@tools_bp.route('/')
def tools_page():
    # 原有静态目录
    static_tools_dir = os.path.join('static', 'tools')
    static_icons_dir = os.path.join('static', 'img', 'tools')

    # 新增的上传目录
    instance_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'instance', 'uploads')
    upload_tools_dir = os.path.join(instance_root, 'tools')
    upload_icons_dir = os.path.join(instance_root, 'img', 'tools')

    # print(upload_tools_dir)
    # print(upload_icons_dir)

    tools = []

    from utils.scan_tools import scan_tools

    # 先扫描 static 目录
    tools.extend(scan_tools(static_tools_dir, static_icons_dir, is_upload=False))

    # 再扫描 instance/uploads 目录
    tools.extend(scan_tools(upload_tools_dir, upload_icons_dir, is_upload=True))

    # 统计各类小程序数量（默认展示全部的统计）
    from collections import Counter
    category_counts = Counter(t['category'] for t in tools)

    total_count = len(tools)

    return render_template('tools.html', tools=tools, total_count=total_count, category_counts=category_counts)
