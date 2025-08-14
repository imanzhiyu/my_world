"""
FilePath: utils/scan_tools.py
Author: Joel
Date: 2025-08-11 20:24:33
LastEditTime: 2025-08-11 20:35:31
Description: 
"""
import os
import glob


def scan_tools(tools_dir, icons_dir, is_upload=False):
    """
    扫描工具exe目录和图标目录
    - tools_dir: exe文件目录
    - icons_dir: 图标文件目录（对应exe的图标目录）
    - is_upload: 是否上传目录标记

    返回列表，每个字典:
    {
      'name': '工具名',
      'icon': 图标路径，上传目录下从uploads/img/tools读取，静态目录从static/img/tools读取，
               但如果找不到图标，则统一返回 'tools/no-pictures.png'（即static/img/tools/no-pictures.png）
      'file': exe文件名,
      'is_upload': True/False
    }
    """
    tools = []
    DEFAULT_ICON = "tools/no-pictures.png"  # 这里是静态目录相对路径，前端通过url_for('static', filename=tool.icon)访问

    for exe_path in glob.glob(os.path.join(tools_dir, '*.exe')):
        base_name = os.path.splitext(os.path.basename(exe_path))[0]  # 文件名不含后缀
        # 尝试找对应图片
        icon_file = None
        for ext in ['png', 'jpg', 'jpeg', 'ico', 'svg']:
            candidate = os.path.join(icons_dir, base_name + '.' + ext)
            if os.path.isfile(candidate):
                # 上传目录的图标，icon路径相对uploads/img/tools目录，但模板中访问时用upload蓝图
                # 静态目录图标，icon路径相对static/img/tools目录，但模板中访问用static蓝图
                icon_file = f"tools/{base_name}.{ext}"
                break
        if not icon_file:
            icon_file = DEFAULT_ICON  # 只有默认图，统一在static/img/tools/no-pictures.png

        tools.append({
            'name': base_name,
            'icon': icon_file,
            'file': os.path.basename(exe_path),
            'is_upload': is_upload,
            'category': '',
        })
    return tools
