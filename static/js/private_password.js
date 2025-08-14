// /**
//  * @FilePath: static/js/private_password.js
//  * @Author: Joel
//  * @Date: 2025-08-11 12:53:20
//  * @LastEditTime: 2025-08-11 15:18:16
//  * @Description:处理密码输入/验证
//  */


function cancelPassword() {
    window.location.href = "/";
}

function showTopError(message) {
    const bar = document.getElementById('topErrorBar');
    bar.textContent = message;
    bar.style.display = 'block';
    setTimeout(() => {
        bar.style.display = 'none';
    }, 4000);
}

// 密码弹窗提交
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('pwdForm');
    form?.addEventListener('submit', e => {
        e.preventDefault();
        submitPassword();
    });
});


// 进入private页面需要密码
function submitPassword() {
    const pwd = document.getElementById('pwdInput').value.trim();
    if (!pwd) {
        showTopError('请输入密码');
        return;
    }
    fetch(PRIVATE_PAGE_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `password=${encodeURIComponent(pwd)}`
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url;
        } else if (response.status === 401) {
            showTopError('密码错误，请重试');
            document.getElementById('pwdInput').value = '';
            document.getElementById('pwdInput').focus();
        } else {
            showTopError('会话已过期，请刷新页面');
        }
    });
}
