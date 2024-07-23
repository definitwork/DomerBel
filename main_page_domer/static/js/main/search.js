const fields = document.querySelector(".fields")
const getCategory = document.querySelector(".main__search-form-item-category")

function getOption(url) {
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if(data.length === 0) return false
      if(data[0].spisok && fields.children.length !== 0) {
        data.forEach(item => {
          if(item?.search.split("|")?.length >= 2 && item?.search.split("|")[0].trim() !== "Марка") {
            createSelectElement(item, item.search.split("|")[0])
            createSelectElement(item, item.search.split("|")[1])
            return
          }
          createSelectElement(item, item.search.split("|")[0].trim())
        })
        return
      }
      createSelectElement(data)
      
    })
    .catch((error) => {
      console.log(error, "error obj")
    })
}

function createSelectElement(
    data, 
    titleObj = {
      id: "",
      title: "Все разделы",
  }
) {
  const select = document.createElement("select")
  select.setAttribute("name", "category__in")
  createOptionElement(titleObj, select)
  
  if(data.spisok && data.spisok !== null) {
    data.spisok.element_set.forEach((item) => {
      createOptionElement(item, select)
    })
    if(titleObj === "Марка") {
      select.addEventListener("change", (event) => {
        const id = event.target.value
        getModel(data, id)
      })
    }
  }else if (!data.spisok && !data.int_val_list) {
    data.forEach((item) => {
      console.log(item);
      createOptionElement(item, select)
    })
    select.addEventListener("change", (event) =>
      getCategoryFunc(event, getOption)
    )
  }else {
    data.int_val_list.forEach(item => {
      createOptionElement(item, select)
    })
  }

  fields.append(select)
}

function getModel(id,data) {
  console.log(data, id);
  const dataModel = new Map(data.spisok)
  console.log(dataModel.size);
}

function createOptionElement(item, parentElement) {
  const option = document.createElement("option")
  option.value = item.id
  option.textContent = item.title || item.title_ad || item
  parentElement.append(option)
}

getCategory.addEventListener("change", (event) => {
  getCategoryFunc(event, getOption)
  fields.innerHTML = ""
})

function getCategoryFunc(event, func) {
  const id = event.target.value
  if(id === "") {
    Array.from(fields.children).forEach((item, index) => {
      if(index !== 0) item.remove()
    })
    return
  }
  if(!func(`http://127.0.0.1:8000/api/v1/categories_for_search/${id}`)) {
    func(`http://127.0.0.1:8000/api/v1/get_field_list/?id=${id}`)
    return
  }
  func(`http://127.0.0.1:8000/api/v1/categories_for_search/${id}`)
}
