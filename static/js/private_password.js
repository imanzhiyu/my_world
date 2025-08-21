// /**
//  * @FilePath: static/js/private_password.js
//  * @Author: Joel
//  * @Date: 2025-08-11 12:53:20
//  * @LastEditTime: 2025-08-21 19:05:28
//  * @Description:处理密码输入/验证
//  */
const privateContent = document.getElementById("privateContent");
const passwordModal = document.getElementById("passwordModal");
const pwdForm = document.getElementById("pwdForm");
const pwdInput = document.getElementById("pwdInput");

function showTopError(message) {
    const bar = document.getElementById('topErrorBar');
    if (!bar) return;
    bar.textContent = message;
    bar.style.display = 'block';
    setTimeout(() => {
        bar.style.display = 'none';
    }, 4000);
}

function cancelPassword() {
    window.location.href = "/";
}

function submitPassword() {
    const pwd = pwdInput.value.trim();
    if (!pwd) {
        showTopError('请输入密码');
        return;
    }

    const formData = new FormData();
    formData.append('password', pwd);

    fetch(PRIVATE_PAGE_URL, {method: 'POST', body: formData})
        .then(res => res.ok ? res.json() : Promise.reject(res))
        .then(data => {
            if (data?.session_id) {
                localStorage.setItem("private_session_id", data.session_id);
                window.location.reload();
            }
        })
        .catch(err => {
            if (err.status === 401) {
                showTopError('密码错误，请重试');
                pwdInput.value = '';
                pwdInput.focus();
            } else {
                console.error(err);
                showTopError('服务器错误，请刷新页面');
            }
        });
}

// 初始化
if (privateContent && passwordModal) {
    const sessionId = localStorage.getItem("private_session_id") || "";
    fetch("/private/check", {method: "GET", headers: {"X-Private-Session": sessionId}})
        .then(res => res.json())
        .then(data => {
            if (data.access) {
                privateContent.style.display = "block";
                passwordModal.style.display = "none";
            } else {
                privateContent.style.display = "none";
                passwordModal.style.display = "flex";
            }
        })
        .catch(err => {
            console.error(err);
            privateContent.style.display = "none";
            passwordModal.style.display = "flex";
        });

    pwdForm?.addEventListener('submit', e => {
        e.preventDefault();
        submitPassword();
    });
    document.querySelector("#passwordModal .button_cancel")?.addEventListener('click', cancelPassword);
}







