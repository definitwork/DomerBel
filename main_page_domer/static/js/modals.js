const login_button = document.querySelector(".login_button");

const popup = document.querySelector(".popup");
const login_popup = document.querySelector(".login_form_popup");
const closing_cross = document.querySelectorAll(".closing_cross");

const register_popup = document.querySelector(".register_form_popup");
const register_button = document.querySelector(".register_button");
const return_to_login_button = document.querySelector(".return_to_login_button");

const forget_popup = document.querySelector(".forget_pass_form_popup");
const forget_button = document.querySelector(".forget_pass_button");
const return_to_login_from_forget = document.querySelector(".return_to_login_from_forget_button");

// -> login

login_button.addEventListener("click", () => {
    popup.style.display = 'flex';
    login_popup.style.display = 'flex';
    forget_button.style.display = 'flex';
    forget_popup.style.display = 'none';

});

closing_cross.forEach(item => item.addEventListener("click", () => {
    popup.style.display = 'none';
    login_popup.style.display = 'none';
    register_popup.style.display = 'none';
    forget_popup.style.display = 'none';
}));

popup.addEventListener("click", (event) => {
    // console.log(event.currentTarget);
    if (event.target === event.currentTarget) {
        popup.style.display = 'none';
        login_popup.style.display = 'none';
        register_popup.style.display = 'none';
        forget_button.style.display = 'none';
    }
});

// -> register

register_button.addEventListener("click", () => {
    login_popup.style.display = 'none';
    register_popup.style.display = 'flex';
});

return_to_login_button.addEventListener("click", () => {
    login_popup.style.display = 'flex';
    register_popup.style.display = 'none';
    forget_button.style.display = 'flex';
});

// -> forget password

forget_button.addEventListener("click", () => {
    login_popup.style.display = 'none';
    forget_popup.style.display = 'flex';
});

return_to_login_from_forget.addEventListener("click", () => {
    login_popup.style.display = 'flex';
    forget_popup.style.display = 'none';
});
