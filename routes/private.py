"""
FilePath: routes/private.py
Author: Joel
Date: 2025-08-10 09:48:08
LastEditTime: 2025-08-16 19:00:54
Description: 
"""
"""
FilePath: routes/private.py
Author: Joel
Date: 2025-08-10 09:48:08
LastEditTime: 2025-08-16 19:00:54
Description: 
"""
from flask import Blueprint, render_template, redirect, url_for, flash, session, request, current_app, jsonify
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename

private_bp = Blueprint('private', __name__)

from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv("PRIVATE_PASSWORD", "000000")
ACCESS_DURATION = timedelta(minutes=int(os.getenv("PRIVATE_ACCESS_DURATION", 15)))  # 15分钟有效期

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # routes 文件夹
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))  # 项目根目录
UPLOAD_ROOT = os.path.join(PROJECT_ROOT, 'instance', 'uploads')

EXE_DIR = os.path.join(UPLOAD_ROOT, 'tools')
IMG_DIR = os.path.join(UPLOAD_ROOT, 'img', 'tools')

if not os.path.exists(UPLOAD_ROOT):
    os.makedirs(UPLOAD_ROOT)
    os.makedirs(EXE_DIR)
    os.makedirs(IMG_DIR)

# print(UPLOAD_ROOT)
# print(EXE_DIR)
# print(IMG_DIR)
# print(PASSWORD)

ALLOWED_EXE_EXTENSIONS = {'exe'}
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'ico', 'svg'}


def allowed_file(filename, allowed_exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts


# ==== 进入private的密码验证 ================================================================================
# token验证，可以跨域
import jwt
import datetime

# 生成 token 的密钥
TOKEN_SECRET = os.getenv("PRIVATE_TOKEN_SECRET", "supersecretkey")
ACCESS_DURATION_MINUTES = ACCESS_DURATION  # 120分钟有效期

import jwt
from datetime import datetime, timedelta


def generate_token():
    exp = datetime.utcnow() + ACCESS_DURATION
    payload = {"exp": exp}
    token = jwt.encode(payload, TOKEN_SECRET, algorithm="HS256")
    # PyJWT >= 2.0 返回 str，不需要 decode
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def verify_token(token):
    try:
        jwt.decode(token, TOKEN_SECRET, algorithms=["HS256"])
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.InvalidTokenError:
        return False


@private_bp.route('/', methods=['GET', 'POST'])
def private_page():
    token = request.args.get('token')
    access = False

    if token and verify_token(token):
        access = True

    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            token = generate_token()
            return redirect(url_for('private.private_page', token=token))
        else:
            return '', 401

    return render_template('private.html', access=access, token=token)


# session验证，无法跨域
# @private_bp.route('/', methods=['GET', 'POST'])
# def private_page():
#     if request.method == 'POST':
#         if request.form.get('password') == PASSWORD:
#             session['private_access'] = True
#             session['private_access_time'] = datetime.utcnow().isoformat()
#             return redirect(url_for('private.private_page'))
#         else:
#             return '', 401
# 
#     access = False
#     access_time_str = session.get('private_access_time')
#     if session.get('private_access') and access_time_str:
#         access_time = datetime.fromisoformat(access_time_str)
#         if datetime.utcnow() - access_time < ACCESS_DURATION:
#             access = True
#         else:
#             session.pop('private_access', None)
#             session.pop('private_access_time', None)
# 
#     return render_template('private.html', access=access)


# === 博客相关 ==========================================================================================

from models.blog import Blog
from models import db


@private_bp.route('/blog', methods=['GET'])
def blog_list():
    posts = Blog.query.order_by(Blog.created_at.desc()).all()
    return render_template('private_blog_list.html', posts=posts)


@private_bp.route('/blog/new', methods=['GET', 'POST'])
def blog_new():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        if not title or not content:
            flash('标题和内容不能为空', 'danger')
            return redirect(url_for('private.blog_new'))
        new_post = Blog(title=title, content=content)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('private.blog_list'))
    return render_template('private_blog_new.html')


@private_bp.route('/blog/<int:post_id>', methods=['GET', 'POST'])
def blog_detail(post_id):
    post = Blog.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form.get('title', '').strip()
        post.content = request.form.get('content', '').strip()
        db.session.commit()
        return redirect(url_for('private.blog_list'))
    return render_template('private_blog_detail.html', post=post)


@private_bp.route('/blog/delete', methods=['POST'])
def blog_delete():
    data = request.get_json()
    ids = data.get('ids', [])
    if not ids:
        return jsonify({'error': '未选择任何博客文章'}), 400

    try:
        Blog.query.filter(Blog.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '删除失败'}), 500


# === 工具相关 ==========================================================================================
import glob


@private_bp.route('/tools')
def private_tools_manage():
    # 复用扫描工具的代码
    static_tools_dir = os.path.join(current_app.root_path, 'static', 'tools')
    static_icons_dir = os.path.join(current_app.root_path, 'static', 'img', 'tools')
    upload_tools_dir = os.path.join(current_app.instance_path, 'uploads', 'tools')
    upload_icons_dir = os.path.join(current_app.instance_path, 'uploads', 'img', 'tools')

    tools = []

    from utils.scan_tools import scan_tools

    tools.extend(scan_tools(static_tools_dir, static_icons_dir, False))
    tools.extend(scan_tools(upload_tools_dir, upload_icons_dir, True))

    total_count = len(tools)

    return render_template('private_tools.html', tools=tools, total_count=total_count)


@private_bp.route('/tools/upload_tool', methods=['POST'])
def upload_tool():
    # # 会话过期拦截
    # access_time_str = session.get('private_access_time')
    # if not session.get('private_access') or not access_time_str:
    #     return jsonify({'error': '会话已过期，请重新输入密码'}), 401
    # access_time = datetime.fromisoformat(access_time_str)
    # if datetime.utcnow() - access_time >= ACCESS_DURATION:
    #     session.pop('private_access', None)
    #     session.pop('private_access_time', None)
    #     return jsonify({'error': '会话已过期，请重新输入密码'}), 401

    # token过期拦截
    token = request.form.get('token') or request.args.get('token')
    if not token or not verify_token(token):
        return jsonify({'error': '会话已过期，请重新输入密码'}), 401

    if 'exeFile' not in request.files:
        return jsonify({'error': '未找到exe文件'}), 400

    exe_file = request.files['exeFile']
    img_file = request.files.get('imgFile', None)

    if exe_file.filename == '' or not allowed_file(exe_file.filename, ALLOWED_EXE_EXTENSIONS):
        return jsonify({'error': '无效的exe文件'}), 400

    exe_filename = secure_filename(exe_file.filename)
    exe_name = exe_filename.rsplit('.', 1)[0]  # 去掉exe后缀的文件名

    # 保存exe文件
    os.makedirs(EXE_DIR, exist_ok=True)
    exe_path = os.path.join(EXE_DIR, exe_filename)
    exe_file.save(exe_path)

    # 处理图片文件，如果有上传
    if img_file and img_file.filename != '':
        if not allowed_file(img_file.filename, ALLOWED_IMAGE_EXTENSIONS):
            return jsonify({'error': '无效的图片文件'}), 400

        img_ext = img_file.filename.rsplit('.', 1)[1].lower()
        img_filename = f"{exe_name}.{img_ext}"
        os.makedirs(IMG_DIR, exist_ok=True)
        img_path = os.path.join(IMG_DIR, img_filename)
        img_file.save(img_path)

    return jsonify({'message': '上传成功'}), 200


@private_bp.route('/tools/delete', methods=['POST'])
def private_tools_delete():
    data = request.get_json()
    tools_to_delete = data.get('tools', [])

    upload_tools_dir = os.path.join(current_app.instance_path, 'uploads', 'tools')
    upload_icons_dir = os.path.join(current_app.instance_path, 'uploads', 'img', 'tools')

    failed = []
    for tool_name in tools_to_delete:
        exe_path = os.path.join(upload_tools_dir, tool_name + '.exe')
        if os.path.exists(exe_path):
            try:
                os.remove(exe_path)
            except Exception:
                failed.append(tool_name)
                continue
        for ext in ['png', 'jpg', 'jpeg', 'ico', 'svg']:
            icon_path = os.path.join(upload_icons_dir, tool_name + '.' + ext)
            if os.path.exists(icon_path):
                try:
                    os.remove(icon_path)
                except:
                    pass
    if failed:
        return jsonify(success=False, message="删除失败：" + ', '.join(failed))
    return jsonify(success=True)


# === 个人信息管理  ==========================================================================================
from models.personal import PersonalInfo


@private_bp.route('/personal', methods=['GET', 'POST'])
def private_personal_edit():
    personal = PersonalInfo.query.first()
    if not personal:
        personal = PersonalInfo()
        db.session.add(personal)
        db.session.commit()

    if request.method == 'POST':
        personal.name = request.form.get('name', '').strip()
        personal.email = request.form.get('email', '').strip()
        personal.bio = request.form.get('bio', '').strip()
        personal.avatar_url = request.form.get('avatar_url', '').strip()
        personal.location = request.form.get('location', '').strip()
        personal.skills = request.form.get('skills', '').strip()

        # 处理动态链接
        names = request.form.getlist('link_name')
        urls = request.form.getlist('link_url')
        links_list = [
            {"name": n.strip(), "url": u.strip()}
            for n, u in zip(names, urls) if n.strip() and u.strip()
        ]
        personal.set_links(links_list)

        try:
            db.session.commit()
            flash('保存成功！', 'success')
            return redirect(url_for('private.private_personal_edit'))
        except Exception as e:
            db.session.rollback()
            flash(f'保存失败: {str(e)}', 'error')

    return render_template('private_personal.html', personal=personal)


# === english corner管理 ==========================================================================================
from models.english import EnglishContent


# list
@private_bp.route('/english', methods=['GET'])
def private_english_list():
    contents = EnglishContent.query.order_by(EnglishContent.updated_at.desc()).all()
    return render_template('private_english_list.html', posts=contents)


# new
@private_bp.route('/english/new', methods=['GET', 'POST'])
def private_english_new():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        if not title or not description:
            flash('标题和描述不能为空', 'error')
        else:
            new_content = EnglishContent(title=title, description=description)
            db.session.add(new_content)
            db.session.commit()
            flash('内容已保存', 'success')
            return redirect(url_for('private.private_english_list'))
    return render_template('private_english_new.html')


# edit
@private_bp.route('/english/edit/<int:content_id>', methods=['GET', 'POST'])
def private_english_detail(content_id):
    content = EnglishContent.query.get_or_404(content_id)
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        if not title or not description:
            flash('标题和描述不能为空', 'error')
        else:
            content.title = title
            content.description = description
            db.session.commit()
            flash('内容已保存', 'success')
            return redirect(url_for('private.private_english_list'))
    return render_template('private_english_detail.html', post=content)


@private_bp.route('/english/delete', methods=['POST'])
def private_english_delete():
    data = request.get_json()
    ids = data.get('ids', [])
    if not ids:
        return jsonify({'error': '未选择任何文章'}), 400

    try:
        EnglishContent.query.filter(EnglishContent.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '删除失败'}), 500


# research管理
from models.research import ResearchContent


# list
@private_bp.route('/research', methods=['GET'])
def private_research_list():
    contents = ResearchContent.query.order_by(ResearchContent.updated_at.desc()).all()
    return render_template('private_research_list.html', posts=contents)


# new
@private_bp.route('/research/new', methods=['GET', 'POST'])
def private_research_new():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        if not title or not description:
            flash('标题和描述不能为空', 'error')
        else:
            new_content = ResearchContent(title=title, description=description)
            db.session.add(new_content)
            db.session.commit()
            flash('内容已保存', 'success')
            return redirect(url_for('private.private_research_list'))
    return render_template('private_research_new.html')


# edit
@private_bp.route('/research/edit/<int:content_id>', methods=['GET', 'POST'])
def private_research_detail(content_id):
    content = ResearchContent.query.get_or_404(content_id)
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        if not title or not description:
            flash('标题和描述不能为空', 'error')
        else:
            content.title = title
            content.description = description
            db.session.commit()
            flash('内容已保存', 'success')
            return redirect(url_for('private.private_research_list'))
    return render_template('private_research_detail.html', post=content)


@private_bp.route('/research/delete', methods=['POST'])
def private_research_delete():
    data = request.get_json()
    ids = data.get('ids', [])
    if not ids:
        return jsonify({'error': '未选择任何文章'}), 400

    try:
        ResearchContent.query.filter(ResearchContent.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'message': '删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '删除失败'}), 500
