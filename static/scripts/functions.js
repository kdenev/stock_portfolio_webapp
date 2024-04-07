function updateData() {
    var myForm = document.forms.form1;
    // Make an AJAX request to the Flask server
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/sort_table', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            // Update the data on the web page
            var dataContainer = document.getElementById('data-container');
            dataContainer.innerHTML = xhr.responseText;
        }
    };
    xhr.onerror = function () {
        console.log('Error!');
    };
    xhr.send(new FormData(myForm));
}