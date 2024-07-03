console.log('hi')
const answer = document.querySelector('#answer');

for (let i of answer.children){
    if (i.id == 'download'){
        console.log(i)
        const buttonDownload = document.querySelector('#download')
        buttonDownload.addEventListener('click', downloadFile)
    }
}

function downloadFile(){
    console.log(11111)
    fetch('http://127.0.0.1:8000/advertisement/download_file_with_error_ads/')
}