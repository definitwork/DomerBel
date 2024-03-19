let region_opened = document.querySelector(".region_opened");
    region_opened.addEventListener('click', show_city);
let get_element_select_city = document.querySelector("#select_city");
let get_element_select_oblast = document.querySelector("#select_oblast");
let get_element_select_category_0 = document.querySelector("#select_category_0");
let region_hidden = document.querySelector(".region_hidden")


function show_city(event){
    if (event.target.value !== "0"){
        fetch(`http://127.0.0.1:8000/api/v1/add_store/city/${event.target.value}`)
            .then((response) => response.json())
            .then(data => {
                region_hidden.style.display = "flex";
                get_element_select_city.innerHTML = `<option value="0">---------</option>`
                get_element_select_city.innerHTML += data.map((elem)=>`<option value=${elem.id}>${elem.area}</option>`)
            })
    }
    else {
        get_element_select_city.innerHTML += "";
        region_hidden.style.display = "none";
    }
}

function show_oblast(){
        fetch(`http://127.0.0.1:8000/api/v1/get_region_list/`)
            .then((response) => response.json())
            .then(data => {
                let array = data.filter(function (i) {
                    return i.level === 0
                })
                // get_element_select_city.innerHTML = `<option value="0">---------</option>`
                get_element_select_oblast.innerHTML += array.map((elem)=> `<option value=${elem.id}>${elem.area}</option>`)
            })
}

show_oblast()


// let get_category = document.querySelector("#select_category");

fetch("http://127.0.0.1:8000/api/v1/get_category_list/")
    .then((response) => response.json())
    .then((data) => {
        console.log(data)
        let array = data.filter(function (i) {
                    return i.level === 0
                })
        console.log(array)
        get_element_select_category_0.innerHTML += array.map((elem)=> `<option value=${elem.id}>${elem.title}</option>`)

    })