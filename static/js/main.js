function openSecondBar() {
    let secondBar = document.getElementById("secondary-bar");
    if ( !secondBar.classList.contains("active") ) {
        secondBar.classList.toggle("active");
    }
}

