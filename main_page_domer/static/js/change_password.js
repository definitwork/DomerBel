document.getElementById("password_person_reset_field").style.display = "none";
document.getElementById("reset_person_pass_button").style.display = "none";
function showFields() {
  document.getElementById("password_person_reset_field").style.display = "flex";
  document.getElementById("reset_person_pass_button").style.display = "flex";
}
document.getElementById("reset_person_pass_click").addEventListener("click", showFields);



document.querySelector('.person_reset_pass_form').addEventListener('submit', function(event) {
  event.preventDefault();
});