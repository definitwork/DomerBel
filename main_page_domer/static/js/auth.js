const form_login_button = document.querySelector('#form_login_button')
const form_register_button = document.querySelector('#form_register_button')
// const send_email_button = document.querySelector('#send_email_button')


form_login_button.addEventListener('click', login_fn)
form_register_button.addEventListener('click', register_fn)
// send_email_button.addEventListener('click', send_email_fn)

const token = getCookie('csrftoken')
console.log('token')

function login_fn() {
    const form_login_data = new FormData(document.querySelector('.login_form'));
    const field_password_login_form = document.querySelector('#password_login_field');
    const login_errors = document.getElementById('login_form_error');
    fetch('http://127.0.0.1:8000/users/login/', {
        method: 'POST',
        headers: {"X-CSRFToken": token},
        body: form_login_data
    })
        .then(response => response.json())
        .then(data => {
                // console.log(data.errors);
                if (data.success) {
                    window.location.href = '/pa';
                } else if (data.errors === 1) {
                    login_errors.innerHTML = 'Неверный email или пароль'
                    field_password_login_form.value = null;
                }
            }
        )
}


// function handleIncorrectInput() {
//     // Генерируем новый URL изображения (например, добавляем случайный хэш)
//     const newCaptchaImageUrl = '/captcha/image/' + '555'; // Замените на реальный URL
//     const captchaImage = document.querySelector('.captcha'); // Замените на реальный ID элемента
//     captchaImage.src = newCaptchaImageUrl;
// }


function register_fn() {
    const form_register_data = new FormData(document.querySelector('#register_form'));
    const error_phone_register = document.querySelector('.error_phone_register');
    const error_email_register = document.querySelector('.error_email_register');
    const error_pass_not_match_register = document.querySelector('.error_pass_not_match_register');
    const error_empty_register = document.querySelector('.error_empty_register');
    const error_captcha_register = document.querySelector('.error_captcha_register');
    // Для обнуленя значений поля
    const field_password2_register_form = document.querySelector('#id_password2');


    fetch('http://127.0.0.1:8000/users/register/', {
        method: 'POST',
        headers: {"X-CSRFToken": token},
        body: form_register_data
    })
        .then(response => response.json())
        .then(data => {
            // if (data.errors.captcha[0] === 'Неверный ответ') {
            //     handleIncorrectInput()
            // }
            console.log(data)
            error_phone_register.innerHTML = data.errors.phone
            error_email_register.innerHTML = data.errors.email
            error_pass_not_match_register.innerHTML = data.errors.password2
            error_empty_register.innerHTML = data.errors.password
            error_captcha_register.innerHTML = data.errors.captcha
        })
}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}