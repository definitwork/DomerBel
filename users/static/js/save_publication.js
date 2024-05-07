const addPublicationButton = document.querySelector(".button_add_publication");
addPublicationButton.addEventListener("click", savePublication);

function savePublication() {
    const form = document.querySelector(".form_add_publication");
    const title = form.querySelector("input[name='title']");
    const announcement = form.querySelector("textarea[name='announcement']");
    const description = form.querySelector("textarea[name='description']");
    const preview_image = form.querySelector("input[name='preview_image']");
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0].value;
    // let data = {
    //     title: title.value,
    //     announcement: announcement.value,
    //     description: description.value,
    //     photo: photo_files.value,

    //   };
    let data = new FormData(form);
    console.log(typeof data);

    fetch(`http://127.0.0.1:8000/api/v1/save_publication/`, {
        method: "POST",
        headers: {
            // "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        // body: JSON.stringify(data),
        body: data,
    })
    .then(response => {
        if (response.ok) {
            console.log("Публикация успешно сохранена.");
            title.value = "";
            announcement.value = "";
            description.value = "";
            preview_image.value = "";
        } else {
            console.log("Ошибка сохранения публикации.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
