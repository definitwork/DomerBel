const selectAll = document.querySelector('.main__info-advertisement-nav-select-all')

selectAll.addEventListener("click", (event) => {
  const checkboxex = document.querySelectorAll('.main__info-advertisement-list-item input[type="checkbox"]')
  checkboxex?.forEach(item => {
    item.checked = event.target.checked
  })
})