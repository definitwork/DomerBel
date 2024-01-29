// document.getElementById("password_person_reset_field").style.display = "none";
// document.getElementById("reset_person_pass_button").style.display = "none";
// document.getElementById("set_new_password").style.display = "none";
//
// function showFields1() {
//     document.getElementById("password_person_reset_field").style.display = "flex";
//     document.getElementById("reset_person_pass_button").style.display = "flex";
// }
//
// function showFields2() {
//     document.getElementById("password_person_reset_field").style.display = "none";
//     document.getElementById("reset_person_pass_button").style.display = "none";
//     document.getElementById("set_new_password").style.display = "flex";
// }
//
// document.getElementById("reset_person_pass_click").addEventListener("click", showFields1);
// document.getElementById("reset_person_pass_button").addEventListener("click", function (event) {
//     event.preventDefault();
//     showFields2();
//     resetPassword();
// });
//
// // document.querySelector('.person_reset_pass_form').addEventListener('submit', function(event) {
// //   event.preventDefault();
// // });
// const token = getCookie('csrftoken')
// function resetPassword() {
//     const password = new FormData(document.querySelector('.person_reset_pass_form'))
//     console.log(password.get('password'))
//     fetch('http://127.0.0.1:8000/users/change_password/', {
//         method: 'POST',
//         headers: {"X-CSRFToken": token},
//         body: new FormData(document.querySelector('.person_reset_pass_form'))
//     })
//         .then(response => response.json())
//         .then(data => {
//             console.log(data)
//         })
// }
//
//
//
