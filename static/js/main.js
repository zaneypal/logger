function openSecondBar(option) {
    let secondBar = document.querySelectorAll(".secondary-bar");
    let mode = '';

    if (option === 'file') {
        mode = "file-options";
    } else if (option === 'edit') {
        mode = "edit-options";
    } else if (option === 'view') {
        mode = "view-options";
    } else if (option === 'format') {
        mode = "format-options";
    } else if (option === 'regex') {
        mode = "regex-edit-options";
    }

    let optionPanel = document.getElementById(mode);

    if (optionPanel.classList.contains("active")) {
        optionPanel.classList.remove("active");
    } else {
        optionPanel.classList.add("active");
    }

    for (let x = 0; x < secondBar.length; x++) {
        if (secondBar[x] === optionPanel) {
            continue;
        }
        secondBar[x].classList.remove("active");
    }
}

function toggleTable(elementID) {
    let tableOption = document.getElementById(elementID);
    tableOption.classList.toggle("active");

    document.getElementById(elementID+'-button').classList.toggle("active");
}

// Upload button changes color when a file is selected
const loggerFile = document.getElementById('loggerfile');
const selectedFileName = document.getElementById('selected-filename')

loggerFile.addEventListener('change', function() {
    selectedFileName.textContent = this.files[0].name;
    document.getElementById('upload-button').classList.add('ready');
})

// Removes red lines under misspelled words
document.querySelectorAll('input[type=text], textarea').forEach(field => field.spellcheck = false);