const registrationForm = document.getElementById("registration_form");
const registrationButton = document.getElementById("registration_button");
registrationButton.addEventListener("click", registration);
const loginForm = document.getElementById("login_form");
const loginButton = document.getElementById("login_button");
loginButton.addEventListener("click", login);
const logoutButton = document.getElementById("logout_button");
logoutButton?.addEventListener("click", logout);
const legal = document.querySelector(".legal");
const physical = document.querySelector(".physical");

function getCookie(name) {
  const cookie = document.cookie.split(";");
  for (let i of cookie) {
    const [cookieName, cookieValue] = i.trim().split("=");
    if (cookieName == name) {
      return cookieValue;
    }
  }
}
/**
 * Sends a registration request to the server.
 *
 * @return {Promise} A promise that resolves with the server response or rejects with an error.
 */

function callbackRecaptcha() {
  registrationButton.addEventListener("click", registration);
}

function expiredCallbackRecaptcha() {
  registrationButton.removeEventListener("click", registration);
}
function registration() {
  const data = new FormData(registrationForm);
  data.append("recaptcha", data.get("g-recaptcha-response"));
  if (legal.classList.contains("modals__signIn-choice-active")) data.append("entity", true);
  fetch("http://127.0.0.1:8000/api/v1/registration_user/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: data,
  })
    .then((resp) => resp.json())
    .then((data) => {
      if (data.errors) {
        throw new Error(JSON.stringify(data.errors));
      }
      if (data.success) {
        const notificationModal = document.querySelector(".modals__notification");
        registrationForm.classList.remove("modal__active");
        notificationModal.classList.add("modal__active");
        const notificationText = document.querySelector(".modals__notification-text");
        notificationText.innerText = data.success;
      }
    })
    .catch((err) => {
      const data = JSON.parse(err.message);
      if (data["recaptcha"]) {
        registrationButton.removeEventListener("click", registration);
      }
      delete data["recaptcha"];
      // reseting recaptcha field
      grecaptcha.reset();
      generatingErrorSField(data, ".modals__signIn");
    });
}
/**
 * Function to generate error messages for input fields based on the provided data.
 *
 * @param {Object} data - An object containing input field names as keys and error messages as values.
 */

function generatingErrorSField(data, fieldForm) {
  for (let i in data) {
    const field = document.querySelector(`${fieldForm} input[name="${i}"]`);
    if (field.parentElement.children.length > 1) field.parentElement.children[0].remove();
    const p = document.createElement("p");
    if (data[i] !== "") {
      p.classList.add("modals__signIn-error");
      p.innerText = data[i];
      field.parentElement.prepend(p);
    }
    field.style.borderColor = "red";
    /**
     * Removes the first child element of the parent element of the field if it exists,
     * and sets the border color of the field to black.
     *
     * @return {void} This function does not return anything.
     */
    field.oninput = () => {
      if (field.parentElement.children.length > 1) field.parentElement.children[0].remove();
      field.style.borderColor = "black";
    };
  }
}

function login() {
  let data = new FormData(loginForm);
  fetch("http://127.0.0.1:8000/api/v1/login_user/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
      //   "Content-Type": "multipart/form-data",
    },
    body: data,
  })
    .then((resp) => {
      if (resp.status === 205) window.location.reload();
      return resp.json();
    })
    .then((data) => {
      console.log(data);
      if (data.errors) throw new Error(JSON.stringify(data.errors));
    })
    .catch((err) => {
      const data = JSON.parse(err.message);
      if (data["recaptcha"]) {
        loginButton.removeEventListener("click", registration);
      }
      delete data["recaptcha"];
      generatingErrorSField(data, ".modals__login");
    });
}

function logout() {
  fetch("http://127.0.0.1:8000/api/v1/logout/", {
    method: "POST",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  }).then((resp) => {
    if (resp.status === 205) window.location.reload();
  });
}
