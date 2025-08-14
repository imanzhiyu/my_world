// /**
//  * @FilePath: static/js/private_research_list.js
//  * @Author: Joel
//  * @Date: 2025-08-13 18:43:12
//  * @LastEditTime: 2025-08-13 18:43:52
//  * @Description:
//  */
document.addEventListener('DOMContentLoaded', () => {
    const selectAllCheckbox = document.getElementById('selectAll');
    const deleteBtn = document.getElementById('deleteSelectedBtn');
    const checkboxes = document.querySelectorAll('.selectBox');

    if (!selectAllCheckbox || !deleteBtn || checkboxes.length === 0) return;

    selectAllCheckbox.addEventListener('change', () => {
        checkboxes.forEach(cb => cb.checked = selectAllCheckbox.checked);
        toggleDeleteButton();
    });

    checkboxes.forEach(cb => {
        cb.addEventListener('change', () => {
            if (!cb.checked) selectAllCheckbox.checked = false;
            else if ([...checkboxes].every(cb => cb.checked)) selectAllCheckbox.checked = true;
            toggleDeleteButton();
        });
    });

    function toggleDeleteButton() {
        const anyChecked = [...checkboxes].some(cb => cb.checked);
        deleteBtn.disabled = !anyChecked;
    }

    deleteBtn.addEventListener('click', () => {
        if (!confirm('确认删除选中的文章吗？此操作不可撤销！')) return;

        const selectedIds = [...checkboxes].filter(cb => cb.checked).map(cb => cb.dataset.id);
        fetch('/private/research/delete', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ids: selectedIds})
        }).then(res => {
            if (res.ok) window.location.reload();
            else alert('删除失败，请稍后重试');
        });
    });
});