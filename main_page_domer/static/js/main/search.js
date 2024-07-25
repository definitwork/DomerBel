const fields = document.querySelector(".fields")
const getCategory = document.querySelector(".main__search-form-item-category")

function getOption(url) {
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      if (data.length === 0) return false
      if (data.some(item => item.spisok !== null && item.spisok !== undefined) && fields.children.length !== 0) {
        data.forEach((item) => {
          if (
            item?.search?.split("|")?.length >= 2 &&
            !item?.spisok?.element_set
          ) {
            createSelectElement(item, item.search.split("|")[0])
            createSelectElement(item, item.search.split("|")[1])
            return
          }
          if (item?.search?.trim() === "") return
          createSelectElement(item, item?.search?.split("|")[0]?.trim())
        })
        return
      }
      if (data.some(item => item.search === "")) return
      createSelectElement(data)
    })
    .catch((error) => {
      console.error(error, "error obj")
    })
}

function getInnerList(data, id) {
  const dataModel = data.spisok.element_set.find((item) => item.id == id)
  if(!dataModel) {
    fields.children[
      Array.from(fields.children).findIndex((item) =>
        item.classList.contains("category__mark")
      )
    ]?.remove()
    return
  }
  createSelectElement(dataModel, data?.title)
}

function createSelectElement(
  data,
  titleObj = {
    id: "",
    title: "Все разделы",
  }
) {
  const select = document.createElement("select")
  if (data[0]?.level) {
    select.setAttribute("name", "category__title__in")
    select.dataset.level = data[0]?.level
  }else {
    select.setAttribute("name", titleObj.title || titleObj)
  }
  createOptionElement(titleObj, select)
  if (data?.spisok && data?.spisok !== null) {
    data.spisok.element_set.forEach((item) => {
      createOptionElement(item, select)
    })
    console.log(111);
    if (
      data?.spisok?.element_set?.some((item) => item?.elementtwo_set && item?.elementtwo_set.length > 0)
    ) {
      console.log(222);
      select.addEventListener("change", (event) => {
        const id = event.target.options[event.target.selectedIndex].dataset.fetchid
        console.log(data)
        getInnerList(data, id)
      })
      select.dataset.active = true
    }
  } else if (!data?.spisok && !data?.int_val_list && !data?.elementtwo_set) {
    console.log(333);
    data?.forEach((item) => {
      createOptionElement(item, select)
    })
    select.addEventListener("change", (event) =>
      getCategoryFunc(event, getOption)
    )
  } else if (data?.elementtwo_set && data?.elementtwo_set.length > 0) {
    console.log(444);
    select.classList.add("category__mark")
    data?.elementtwo_set.forEach((item) => {
      createOptionElement(item, select)
    })
    fields.children[
      Array.from(fields.children).findIndex((item) =>
        item.classList.contains("category__mark")
      )
    ]?.remove()
    const actionSelectIndex = Array.from(fields.children).findIndex(
      (item) => item.dataset.active === "true"
    )
    fields.insertBefore(select, fields.children[actionSelectIndex + 1])
    return
  } else if(data?.max_val_interval_date !== 0) {
    console.log(555);
    for(let i = data.max_val_interval_date; i >= data.min_val_interval_date ; i--){
      createOptionElement(i, select)
    }
  } else {
    console.log(666);
    if (data.search === null || !data.search) {
      fields.children[
        Array.from(fields.children).findIndex((item) =>
          item.classList.contains("category__mark")
        )
      ]?.remove()
      return
    }
    data?.int_val_list?.forEach((item) => {
      createOptionElement(item, select)
    })
  }

  fields.append(select)
}

function createOptionElement(item, parentElement) {
  const option = document.createElement("option")
  option.value = item.title
  option.dataset.fetchid = item.id
  option.textContent = item.title || item.title_ad || item
  parentElement.append(option)
}

getCategory.addEventListener("change", (event) => {
  getCategoryFunc(event, getOption)
  fields.innerHTML = ""
})

function getCategoryFunc(event, func) {
  const id = event.target.options[event.target.selectedIndex].dataset.fetchid
  const filterFields = Array.from(fields.children).filter(
    (item) =>
      !item.dataset.level || item.dataset.level > event.target.dataset.level
  )
  if(event.target.dataset.level && fields.children.length > 1){
    for(let item of filterFields){
      item.remove()
    }
    if(event.target.dataset.level && event.target.value === ""){
      return
    }
  }
  
  if (!func(`http://127.0.0.1:8000/api/v1/categories_for_search/${id}`)) {
    func(`http://127.0.0.1:8000/api/v1/get_field_list/?id=${id}`)
  }else{
    func(`http://127.0.0.1:8000/api/v1/categories_for_search/${id}`)
  }
}
