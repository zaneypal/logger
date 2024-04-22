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
    const logView = document.querySelectorAll('.log-view');
    const tableButton = document.querySelectorAll('.table-btn');
    const currentButton = document.getElementById(elementID+'-btn');
    
    if (window.location.href.includes('/loggersession/')) {
        for (let x = 0; x < logView.length; x++) {
            if (logView[x] === tableOption) {
                logView[x].classList.toggle("active");
            }
        }
        currentButton.classList.toggle("active");
    } else {
        for (let x = 0; x < logView.length; x++) {
            if (logView[x] === tableOption) {
                logView[x].classList.toggle("active");
            } else {
                logView[x].classList.remove("active");
            }
        }
    
        for (let x = 0; x < tableButton.length; x++) {
            if (tableButton[x] === currentButton) {
                tableButton[x].classList.toggle("active");
            } else {
                tableButton[x].classList.remove("active");
            }
        }
    }
}

const submitButton = document.getElementById("submit-btn");
function activateButton() {
    if (document.getElementById("paste-logs-field").value === "") {
        submitButton.classList.remove("ready");
    } else {
        submitButton.classList.add("ready");
    }
}

function openPanel(option, suboption) {
    document.getElementById('overlay').classList.add("on");

    if (option === 'fields-editor') {
        document.getElementById('fields-editor').classList.add("ready");
        if (suboption === 'configure') {
            document.getElementById('configure-fields-interface').classList.add("ready");
        } else if (suboption === 'add') {
            document.getElementById('add-fields-interface').classList.add("ready");
        }
    }
}

// Upload button changes color when a file is selected
const loggerFile = document.getElementById('loggerfile');
const selectedFileName = document.getElementById('selected-filename');
const uploadButton = document.getElementById('upload-button');

loggerFile.addEventListener('change', function() {
    selectedFileName.textContent = this.files[0].name;
    uploadButton.classList.add('ready');
    
    if (uploadOptionText.checked === true && headerFormat.value === '') {
        uploadButton.classList.remove('ready');
    }
})

const uploadOptionText = document.getElementById('upload-option3'); 
const uploadOption = document.getElementById('upload-option2'); 
const headerFormat = document.getElementById('upload-option-other');
uploadOptionText.addEventListener('mouseup', function() {
    headerFormat.disabled = false;
    uploadButton.classList.remove('ready')
})

document.querySelector('label[for="upload-option3"]').addEventListener('mouseup', function() {
    headerFormat.disabled = false;
    uploadButton.classList.remove('ready')
})

uploadOption.addEventListener('mouseup', function() {
    headerFormat.disabled = true;
    if (loggerFile.value != '') {
        uploadButton.classList.add('ready');
    }
})

document.querySelector('label[for="upload-option2"]').addEventListener('mouseup', function() {
    headerFormat.disabled = true;
    if (loggerFile.value != '') {
        uploadButton.classList.add('ready');
    }
})

headerFormat.addEventListener('input', function() {
    if (headerFormat.value === '') {
        uploadButton.classList.remove('ready');
    } else {
        if (loggerFile.value != '') {
            uploadButton.classList.add('ready');
        }
    }
})

// Removes red lines under misspelled words
document.querySelectorAll('input[type=text], textarea').forEach(field => field.spellcheck = false);