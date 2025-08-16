// /**
//  * @FilePath: static/js/private_upload_tool.js
//  * @Author: Joel
//  * @Date: 2025-08-11 12:53:44
//  * @LastEditTime: 2025-08-16 19:09:44
//  * @Description:上传小工具弹窗逻辑
//  */


document.addEventListener('DOMContentLoaded', () => {
    const uploadCard = document.getElementById('addToolCard');
    const uploadModal = document.getElementById('uploadModal');
    const uploadForm = document.getElementById('uploadForm');

    // EXE 文件相关
    const exeInputHidden = document.getElementById('exeFile');
    const exePathDisplay = document.getElementById('exeFilePath');
    const exeSelectBtn = document.getElementById('exeSelectBtn');

    // IMG 文件相关（可选）
    const imgInputHidden = document.getElementById('imgFile');
    const imgPathDisplay = document.getElementById('imgFilePath');
    const imgSelectBtn = document.getElementById('imgSelectBtn');

    // 上传按钮
    const uploadBtn = document.querySelector('#uploadForm .button_submit');

    /** 更新上传按钮状态 */
    function updateUploadButtonState() {
        uploadBtn.disabled = exeInputHidden.files.length === 0;
    }

    /** 文件路径回显 */
    function updateFilePath(input, display) {
        if (input.files.length > 0) {
            display.value = input.files[0].name;
        } else {
            display.value = '';
        }
    }

    /** 打开弹窗 */
    if (uploadCard) {
        uploadCard.addEventListener('click', () => {
            uploadModal.style.display = 'flex';
            updateUploadButtonState();
        });
    }


    /** 关闭弹窗并重置表单 */
    window.closeUploadModal = function () {
        uploadModal.style.display = 'none';
        uploadForm.reset();
        exePathDisplay.value = '';
        imgPathDisplay.value = '';
        updateUploadButtonState();
    };

    // 文件选择按钮事件
    exeSelectBtn?.addEventListener('click', () => exeInputHidden.click());
    imgSelectBtn?.addEventListener('click', () => imgInputHidden.click());

    // 文件选择回显
    exeInputHidden?.addEventListener('change', () => {
        updateFilePath(exeInputHidden, exePathDisplay);
        updateUploadButtonState();
    });
    imgInputHidden?.addEventListener('change', () => {
        updateFilePath(imgInputHidden, imgPathDisplay);
    });

    // 提交上传
    uploadForm?.addEventListener('submit', async e => {
        e.preventDefault();

        if (exeInputHidden.files.length === 0) {
            alert('请先选择 EXE 文件');
            return;
        }
        // ✅ 先检查 token
        if (!PRIVATE_TOKEN) {
            alert('会话已过期，请先输入密码');
            window.location.reload();  // 刷新页面，让用户重新获取 token
            return;
        }

        const formData = new FormData();
        formData.append('exeFile', exeInputHidden.files[0]);
        if (imgInputHidden.files.length > 0) {
            formData.append('imgFile', imgInputHidden.files[0]);
        }

        // ✅ 在这里加上 token
        formData.append('token', PRIVATE_TOKEN);

        try {
            const res = await fetch(UPLOAD_TOOL_URL, {
                method: 'POST',
                body: formData,
            });
            if (res.status === 401) {
                alert('会话已过期，请重新输入密码');
                window.location.reload();
                return;
            }
            if (res.ok) {
                alert('上传成功！');
                closeUploadModal();
                window.location.reload();  // 上传成功后刷新页面
            } else {
                const err = await res.json();
                alert(err.error || '上传失败，请重试');
            }
        } catch (e) {
            alert('上传发生错误');
            console.error(e);
        }

    });


});

