let region_oblast = document.querySelector(".region_oblast");
    region_oblast.addEventListener('click', show_city);
let get_element_select_city = document.querySelector("#select_city");


function show_city(event){
    if (event.target.value !== "0"){
        fetch(`http://127.0.0.1:8000/api/v1/add_store/city/${event.target.value}`)
            .then((response) => response.json())
            .then(data => {
                get_element_select_city.innerHTML = `<option value="0">---------</option>`
                get_element_select_city.innerHTML += data.map((elem)=>`<option value=${elem.id}>${elem.area}</option>`)
            })
    }
    else {
        get_element_select_city.innerHTML = `<option value="0">---------</option>`;
    }
}