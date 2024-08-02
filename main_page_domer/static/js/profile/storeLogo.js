const logoInput = document.getElementById('id_logo_image')
const logoLabel = document.querySelector(".main__info label[for='id_logo_image']")
const closeTag = document.querySelector(".cross")
logoInput.addEventListener('change', (event) => {
  const profileImg = document.querySelectorAll(".profile__logo-img")
  if(profileImg.length >= 1) {
    Array.from(profileImg).forEach((item) => {
      item.remove()
    })
  }
  const file = event.target.files[0];
  const reader = new FileReader();
  reader.readAsDataURL(file)
  reader.onload = (e) => {
    const div = document.createElement('div');
    div.classList.add("profile__logo-img")
    const cross = document.createElement('div');
    cross.classList.add("cross");
    cross.innerHTML = "X"
    const img = document.createElement('img');
    img.src = e.target.result
    div.append(img)
    div.append(cross)
    logoLabel.after(div)
    cross.addEventListener('click', (event) => {
      event.target.parentElement.remove()
      logoInput.value = ""
    })
  }
})
