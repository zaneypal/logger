function openSecondBar() {
    let secondBar = document.getElementById("secondary-bar");
    if ( !secondBar.classList.contains("active") ) {
        secondBar.classList.toggle("active");
    }
}

const loggerFile = document.getElementById('loggerfile');
const selectedFileName = document.getElementById('selected-filename')

loggerFile.addEventListener('change', function() {
    selectedFileName.textContent = this.files[0].name;
    document.getElementById('upload-button').classList.add('ready');
})

console.log("Hi " + event.target.files[0].name);
