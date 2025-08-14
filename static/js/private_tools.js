// /**
//  * @FilePath: static/js/private_tools.js
//  * @Author: Joel
//  * @Date: 2025-08-11 17:21:05
//  * @LastEditTime: 2025-08-13 14:11:03
//  * @Description:
//  */


// 工具管理页逻辑
document.addEventListener('DOMContentLoaded', () => {
    const deleteBtn = document.getElementById('deleteSelectedBtn');
    const addBtn = document.getElementById('addToolBtn');
    const toolsManageList = document.getElementById('toolsManageList');

    // 检查是否有复选框勾选
    const updateDeleteBtnState = () => {
        const anyChecked = document.querySelectorAll('.select-tool:checked').length > 0;
        deleteBtn.disabled = !anyChecked;
    };

    // 初始化状态
    updateDeleteBtnState();

    // 监听复选框变化
    toolsManageList.addEventListener('change', (e) => {
        if (e.target.classList.contains('select-tool')) {
            updateDeleteBtnState();
        }
    });

    // 点击卡片切换选中状态（避免点击复选框本身时重复触发）
    toolsManageList.addEventListener('click', (e) => {
        const card = e.target.closest('.tool-card');
        if (card && !e.target.classList.contains('select-tool')) {
            const checkbox = card.querySelector('.select-tool');
            if (checkbox) {
                checkbox.checked = !checkbox.checked;
                updateDeleteBtnState();
            }
        }
    });

    // 删除选中工具
    deleteBtn.addEventListener('click', () => {
        const selectedTools = [...document.querySelectorAll('.select-tool:checked')];
        if (selectedTools.length === 0) {
            alert('请选择要删除的工具');
            return;
        }
        if (!confirm(`确定删除选中的 ${selectedTools.length} 个工具吗？此操作不可撤销！`)) return;

        const toolNames = selectedTools.map(cb => cb.closest('.tool-card').dataset.id);

        fetch('/private/tools/delete', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({tools: toolNames})
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert('删除成功！');
                    window.location.reload();
                } else {
                    alert('删除失败: ' + data.message);
                }
            });
    });

    // 新增按钮
    addBtn.addEventListener('click', () => {
        const uploadModal = document.getElementById('uploadModal');
        if (uploadModal) {
            uploadModal.style.display = 'flex';
        } else {
            alert('上传弹窗未找到，请确认模板是否正确引入');
        }
    });
});

