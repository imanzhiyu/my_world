// /**
//  * @FilePath: static/js/private_textarea_editor.js
//  * @Author: Joel
//  * @Date: 2025-08-20 19:05:56
//  * @LastEditTime: 2025-08-21 15:54:10
//  * @Description:
//  */

// ======== 自定义字体和字号 whitelist ========
var Size = Quill.import('attributors/style/size');
Size.whitelist = Array.from({length: 27}, (_, i) => (i + 10) + 'px');
Quill.register(Size, true);

var Font = Quill.import('formats/font');
const fonts = [
    {value: '', label: '微软雅黑'},
    {value: 'simhei', label: '黑体'},
    {value: 'simsun', label: '宋体'},
    {value: 'fangsong', label: '伪宋'},
    {value: 'youyuan', label: '幼圆'},
    {value: 'serif', label: '衬线'},
    {value: 'monospace', label: '等宽'},
    {value: 'arial', label: 'Arial'},
    {value: 'times-new-roman', label: 'Times New Roman'},
    {value: 'courier-new', label: 'Courier New'},
    {value: 'georgia', label: 'Georgia'},
    {value: 'verdana', label: 'Verdana'},
    {value: 'tahoma', label: 'Tahoma'},
    {value: 'comic-sans-ms', label: 'Comic Sans MS'}
];
Font.whitelist = fonts.map(f => f.value);
Quill.register(Font, true);

// ======== 工具栏配置 ========
var toolbarOptions = [
    [{'header': [1, 2, 3, false]}],
    ['bold', 'italic', 'underline', 'strike'],
    [{'color': []}, {'background': []}],
    [{'align': []}],
    [{'list': 'ordered'}, {'list': 'bullet'}],
    [{'indent': '-1'}, {'indent': '+1'}],
    ['blockquote', 'code-block'],
    ['link'],// 'image','video'],
    [{'font': fonts.map(f => f.value)}],
    [{'size': Size.whitelist}],
    ['clean']
];

// ======== 初始化 Quill ========
var quill = new Quill('#editor', {
    theme: 'snow',
    placeholder: '开始写作吧...',
    modules: {
        toolbar: {
            container: toolbarOptions,
            handlers: {
                'link': function (value) {
                    if (value) {
                        let href = prompt('请输入链接地址:');
                        if (href) {
                            const range = this.quill.getSelection();
                            if (range && range.length > 0) {
                                this.quill.format('link', href);
                            } else {
                                this.quill.insertText(range.index, href, 'link', href);
                            }
                        }
                    } else {
                        this.quill.format('link', false);
                    }
                }
            }
        }
    }
});

// ======== 提交保存 HTML 内容到 textarea ========
// 公共表单提交逻辑
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    if (!form) return;

    form.onsubmit = function () {
        // 如果页面有 #content，就写入 #content
        const contentField = document.querySelector("#content");
        if (contentField) {
            contentField.value = quill.root.innerHTML;
        }

        // 如果页面有 #bio，就写入 #bio
        const bioField = document.querySelector("#bio");
        if (bioField) {
            bioField.value = quill.root.innerHTML;
        }
    };
});


// ======== 自定义下拉显示文字 ========
const headerLabels = {'1': '标题1', '2': '标题2', '3': '标题3', 'false': '正文'};
document.querySelectorAll('.ql-header .ql-picker-item').forEach(item => {
    const value = item.getAttribute('data-value') || 'false';
    item.setAttribute('data-label', headerLabels[value]);
});
document.querySelector('.ql-header .ql-picker-label').setAttribute('data-label', '正文');

document.querySelectorAll('.ql-size .ql-picker-item').forEach(item => {
    const val = item.getAttribute('data-value');
    if (val) {
        const num = parseInt(val.replace('px', ''));
        if (!isNaN(num)) item.setAttribute('data-label', num);
    }
});
document.querySelector('.ql-size .ql-picker-label').setAttribute('data-label', '18');

document.querySelectorAll('.ql-font .ql-picker-item').forEach(item => {
    const val = item.getAttribute('data-value');
    const match = fonts.find(f => f.value === val);
    if (match) item.setAttribute('data-label', match.label);
});
document.querySelector('.ql-font .ql-picker-label').setAttribute('data-label', '微软雅黑');


document.addEventListener('DOMContentLoaded', () => {
    const editorContainer = document.getElementById('editor');
    if (!editorContainer) return; // 如果没有编辑器，直接返回

    // 创建右上角全屏按钮
    const fullscreenBtn = document.createElement('button');
    fullscreenBtn.id = 'fullscreen-btn';
    fullscreenBtn.type = 'button'; // 防止触发表单提交
    fullscreenBtn.title = '全屏/退出全屏';
    fullscreenBtn.innerText = '⛶'; // 默认全屏符号
    fullscreenBtn.style.position = 'absolute';
    fullscreenBtn.style.top = '2px';
    fullscreenBtn.style.right = '7px';
    fullscreenBtn.style.zIndex = '1001';
    fullscreenBtn.style.cursor = 'pointer';
    fullscreenBtn.style.background = 'transparent';
    fullscreenBtn.style.border = 'none';
    fullscreenBtn.style.fontSize = '18px';
    editorContainer.style.position = 'relative';
    editorContainer.appendChild(fullscreenBtn);

    // 点击切换全屏
    fullscreenBtn.addEventListener('click', () => {
        editorContainer.classList.toggle('ql-fullscreen');
        fullscreenBtn.innerText = editorContainer.classList.contains('ql-fullscreen') ? '🗗' : '⛶';
    });
});

// 单独处理人员编辑页面
document.addEventListener("DOMContentLoaded", function () {
    const bioField = document.getElementById("bio");
    if (bioField && bioField.value) {
        // 用 Quill API 插入 HTML，而不是当纯文本
        quill.clipboard.dangerouslyPasteHTML(bioField.value);
    }
});


// ======== hover tooltip 提示 ========
const tooltips = {
    '.ql-bold': '加粗',
    '.ql-italic': '斜体',
    '.ql-underline': '下划线',
    '.ql-strike': '删除线',
    '.ql-color': '字体颜色',
    '.ql-background': '背景色',
    '.ql-align': '对齐',
    '.ql-list[value="ordered"]': '有序列表',
    '.ql-list[value="bullet"]': '无序列表',
    '.ql-indent[value="-1"]': '减少缩进',
    '.ql-indent[value="+1"]': '增加缩进',
    '.ql-blockquote': '引用',
    '.ql-code-block': '代码块',
    '.ql-link': '插入链接',
    '.ql-image': '插入图片',
    '.ql-video': '插入视频',
    '.ql-clean': '清除格式'
};
const tooltip = document.getElementById('tooltip');
Object.keys(tooltips).forEach(selector => {
    document.querySelectorAll(selector).forEach(btn => {
        btn.addEventListener('mouseenter', e => {
            tooltip.innerText = tooltips[selector];
            const rect = btn.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.top - 30) + 'px';
            tooltip.style.display = 'block';
        });
        btn.addEventListener('mouseleave', () => {
            tooltip.style.display = 'none';
        });
    });
});


