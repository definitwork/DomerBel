const registrationForm = document.getElementById("registration_form")
const registrationButton = document.getElementById("registration_button")
      registrationButton.addEventListener("click", registration)
const loginForm = document.getElementById("login_form")
const loginButton = document.getElementById("login_button")
      loginButton.addEventListener("click", login)
// const logoutButton = document.getElementById('logout_button')
//       logoutButton.addEventListener('click', logout)

function getCookie(name) {
    const cookie = document.cookie.split(';')
    for (let i of cookie) {
        const [cookieName, cookieValue] = i.trim().split('=');
        if (cookieName == name) {
            return cookieValue
        }
    }
}


function registration() {
    let data = new FormData(registrationForm)
    data.append("recaptcha", data.get('g-recaptcha-response'))
    fetch("http://127.0.0.1:8000/api/v1/registration_user/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            // "Content-Type": "multipart/form-data",
        }, body: data,
    })
        .then((resp) => resp.json())
        .then((data) => {
            console.log(data)
        })
}


function login() {
    let data = new FormData(loginForm)
    fetch("http://127.0.0.1:8000/api/v1/login_user/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            // "Content-Type": "multipart/form-data",
        }, body: data,
    })
        .then((resp) => resp.json())
        .then((data) => {
            console.log(data)
        })
}


function logout() {
    fetch("http://127.0.0.1:8000/api/v1/logout/", {
        method: "GET",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
}
