const fields = document.querySelector(".fields")
const getCategory = document.querySelector(".main__search-form-item-category")

function getOption(url) {
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.length === 0) return false
      if (data[0].spisok && fields.children.length !== 0) {
        data.forEach((item) => {
          console.log(item);
          if (
            item?.search.split("|")?.length >= 2 
            &&
            !item?.spisok?.element_set
          ) {
            createSelectElement(item, item.search.split("|")[0])
            createSelectElement(item, item.search.split("|")[1])
            return
          }
          if (item.search.trim() === "") return
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

function getInnerList(data, id) {
  const dataModel = data.spisok.element_set.find((item) => item.id == id)
  console.log(data, 'datamodel');
  createSelectElement(dataModel, data?.search?.split("|")[1]?.trim())
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
  if (data?.spisok && data?.spisok !== null) {
    data.spisok.element_set.forEach((item) => {
      createOptionElement(item, select)
    })
    if (data.spisok.element_set[0]?.elementtwo_set) {
      select.addEventListener("change", (event) => {
        const id = event.target.value
        getInnerList(data, id)
      })
      select.dataset.active = true
    }
  } else if (!data?.spisok && !data?.int_val_list && !data.elementtwo_set) {
    data.forEach((item) => {
      createOptionElement(item, select)
    })
    select.addEventListener("change", (event) =>
      getCategoryFunc(event, getOption)
    )
  } else if (data?.elementtwo_set) {
    console.log(data);
    select.classList.add("category__mark")
    data?.elementtwo_set.forEach((item) => {
      createOptionElement(item, select)
    })
    fields.children[
      Array.from(fields.children).findIndex((item) =>
        item.classList.contains("category__mark")
      )
    ]?.remove()
    console.log(fields.children);
    console.log(Array.from(fields.children).findIndex(item => {
      console.log(item.dataset.active === "true");
    }));
    fields.insertBefore(select, fields.children[2])
    return
  } else {
    data?.int_val_list.forEach((item) => {
      createOptionElement(item, select)
    })
  }

  fields.append(select)
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
  if (id === "") {
    Array.from(fields.children).forEach((item, index) => {
      if (index !== 0) item.remove()
    })
    return
  }
  if (!func(`http://127.0.0.1:8000/api/v1/categories_for_search/${id}`)) {
    func(`http://127.0.0.1:8000/api/v1/get_field_list/?id=${id}`)
    return
  }
  func(`http://127.0.0.1:8000/api/v1/categories_for_search/${id}`)
}
