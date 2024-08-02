const regionSelect = document.querySelector(".main__info select[name='region']")
regionSelect?.addEventListener("change", (event) => {
  fetch(`http://127.0.0.1:8000/api/v1/get_city_list/${event.target.value}`)
    .then(resp => resp.json())
    .then(data => {
      createSelectElement(
        data, 
        {id: "", title: "Любое расположение"}, 
        regionSelect, 
        false
      )
    })
    .catch(err => console.error(err))
})

