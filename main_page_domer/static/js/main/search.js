
function getOption(url) {
  fetch(url)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => {
      console.log(error, "error obj");
    });
}

getOption("http://127.0.0.1:8000/api/v1/get_category_list/");

function addOption(parent, arr) {}
