const form_login_button = document.querySelector('#form_login_button');
const form_register_button_entity = document.querySelector('.form_register_button_entity');
const form_register_button_individual = document.querySelector('.form_register_button_individual');
const error_name_register = document.getElementById('error_name_register');
const error_phone_register = document.getElementById('error_phone_register');
const error_email_register = document.getElementById('error_email_register');
const error_pass_not_match_register = document.getElementById('error_pass_not_match_register');
const error_bad_password_register = document.getElementById('error_bad_password_register');
const error_click_captcha = document.getElementById('error_click_captcha');
const error_name_register1 = document.getElementById('error_name_register1');
const error_phone_register1 = document.getElementById('error_phone_register1');
const error_email_register1 = document.getElementById('error_email_register1');
const error_pass_not_match_register1 = document.getElementById('error_pass_not_match_register1');
const error_bad_password_register1 = document.getElementById('error_bad_password_register1');
const error_click_captcha1 = document.getElementById('error_click_captcha1');
const info_massage_popup = document.querySelector('.info_massage_popup');
// Для обнуленя getElementById
const field_password2_register_form = document.querySelector('#id_password2');

function checkForEnter(event) {
    if (event.key === "Enter") {
        console.log('yyyyyyyyy')
        // Выполните действия, которые должны произойти при нажатии Enter
        // Например, отправьте форму:
        document.getElementById("register_form_individual, register_form_entity, form_login_button").submit();
    }
}



form_login_button.addEventListener('click', login_fn)
form_register_button_individual.addEventListener('click', register_fn1)
form_register_button_entity.addEventListener('click', register_fn2)



const token = getCookie('csrftoken')

function login_fn() {
    const form_login_data = new FormData(document.querySelector('.login_form'));
    const field_password_login_form = document.querySelector('#password_login_field');
    const login_errors = document.querySelector('#login_form_error');
    fetch('http://127.0.0.1:8000/users/login/', {
        method: 'POST',
        headers: {"X-CSRFToken": token},
        body: form_login_data
    })
        .then(response => response.json())
        .then(data => {
                console.log(data.errors);
                if (data.success) {
                    window.location.href = 'http://127.0.0.1:8000/users/personal_account/';
                } else if (data.errors === 1) {
                    login_errors.innerHTML = 'Неверный email или пароль'
                    field_password_login_form.value = null;
                }
            }
        )
}





function register_fn1() {
    fetch('http://127.0.0.1:8000/users/register_individual/', {
        method: 'POST',
        headers: {"X-CSRFToken": token},
        body: new FormData(document.querySelector('#register_form_individual'))
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.success) {
                window.location.href = 'http://127.0.0.1:8000/register_done';
                info_massage_popup.style.display = 'flex';
            }

            if (data.errors) {
                reset()
            }

            if (data.errors.name) {
                error_name_register.innerHTML = data.errors.name;
                const name_individual_field = document.getElementById('name_individual_field');
                name_individual_field.style.border = '1px solid red';
               

            } else {
                error_name_register.innerHTML = ''
            }

            if (data.errors.phone) {
                error_phone_register.innerHTML = data.errors.phone;
                const name_individual_field = document.getElementById('phone_individual_field');
                name_individual_field.style.border = '1px solid red';
            } else {
                error_phone_register.innerHTML = '';
            }
            if (data.errors.email) {
                error_email_register.innerHTML = data.errors.email;
                const email_individual_field = document.getElementById('email_individual_field');
                email_individual_field.style.border = '1px solid red';
            } else {
                error_email_register.innerHTML = '';
            }
            if (data.errors.password) {
                error_bad_password_register.innerHTML = data.errors.password;
                const password_individual_field = document.getElementById('password_individual_field');
                password_individual_field.style.border = '1px solid red';
            } else {
                error_bad_password_register.innerHTML = '';
            }
            if (data.errors.password2) {
                error_pass_not_match_register.innerHTML = data.errors.password2;
                const password2_individual_field = document.getElementById('password2_individual_field');
                password2_individual_field.style.border = '1px solid red';
                field_password2_register_form.value = null
            } else {
                error_pass_not_match_register.innerHTML = '';
            }
            if (data.errors.captcha) {
                error_click_captcha.innerHTML = data.errors.captcha;
            } else {
                error_click_captcha.innerHTML = '';
            }
        })
}
name_individual_field.addEventListener('input', () => {
    name_individual_field.style.border = '1px solid black';
    error_name_register.innerHTML = '';
});
email_individual_field.addEventListener('input', () => {
    email_individual_field.style.border = '1px solid black';
    error_email_register.innerHTML = '';
});
phone_individual_field.addEventListener('input', () => {
    phone_individual_field.style.border = '1px solid black';
    error_phone_register.innerHTML = '';
});
password_individual_field.addEventListener('input', () => {
    password_individual_field.style.border = '1px solid black';
    error_bad_password_register.innerHTML = '';
    
});
password2_individual_field.addEventListener('input', () => {
    password2_individual_field.style.border = '1px solid black';
    error_pass_not_match_register.innerHTML = '';
});




function register_fn2() {
    fetch('http://127.0.0.1:8000/users/register_entity/', {
        method: 'POST',
        headers: {"X-CSRFToken": token},
        body: new FormData(document.querySelector('#register_form_entity'))
        
    })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.success) {
                window.location.href = 'http://127.0.0.1:8000/register_done';
                info_massage_popup.style.display = 'flex';
            }

            if (data.errors) {
                reset()
            }

            if (data.errors.name) {
                error_name_register1.innerHTML = data.errors.name;
                const name_entity_field = document.getElementById('name_entity_field');
                name_entity_field.style.border = '1px solid red';
            } else {
                error_name_register1.innerHTML = ''
            }

            if (data.errors.phone) {
                error_phone_register1.innerHTML = data.errors.phone;
                const phone_entity_field = document.getElementById('phone_entity_field');
                phone_entity_field.style.border = '1px solid red';
            } else {
                error_phone_register1.innerHTML = '';
            }
            if (data.errors.email) {
                error_email_register1.innerHTML = data.errors.email;
                const email_entity_field = document.getElementById('email_entity_field');
                email_entity_field.style.border = '1px solid red';
            } else {
                error_email_register1.innerHTML = '';
            }
            if (data.errors.password) {
                error_bad_password_register1.innerHTML = data.errors.password;
                const password_entity_field = document.getElementById('password_entity_field');
                password_entity_field.style.border = '1px solid red';
            } else {
                error_bad_password_register1.innerHTML = '';
            }
            if (data.errors.password2) {
                error_pass_not_match_register1.innerHTML = data.errors.password2;
                const password2_entity_field = document.getElementById('password2_entity_field');
                password2_entity_field.style.border = '1px solid red';
                field_password2_register_form.value = null
            } else {
                error_pass_not_match_register1.innerHTML = '';
            }
            if (data.errors.captcha) {
                error_click_captcha1.innerHTML = data.errors.captcha;
            } else {
                error_click_captcha1.innerHTML = '';
            }

        })
}

name_entity_field.addEventListener('input', () => {
    name_entity_field.style.border = '1px solid black';
    error_name_register1.innerHTML = '';
});
email_entity_field.addEventListener('input', () => {
    email_entity_field.style.border = '1px solid black';
    error_email_register1.innerHTML = '';

});
phone_entity_field.addEventListener('input', () => {
    phone_entity_field.style.border = '1px solid black';
    error_phone_register1.innerHTML = '';

});
password_entity_field.addEventListener('input', () => {
    password_entity_field.style.border = '1px solid black';
    error_bad_password_register1.innerHTML = '';

});
password2_entity_field.addEventListener('input', () => {
    password2_entity_field.style.border = '1px solid black';
    error_pass_not_match_register1.innerHTML = '';

});

setTimeout(function() {
    info_massage_popup.style.display = "none";
    window.location.href = 'http://127.0.0.1:8000'
}, 5000);


function reset() {
    grecaptcha.reset();
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
    return cookieValue
}
