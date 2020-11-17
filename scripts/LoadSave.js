//run server-side code to retrieve needed data
function loadData() {
    fetch('http://example.com/data.json') //change this to where the data is stored
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            console.log(JSON.stringify(myJson));
        });
}


//insert it into static page templates
var htmlElem = document.querySelector('html');
var pElem = document.querySelector('p');

var textForm = document.getElementById('text');
var fontForm = document.getElementById('font');

if(!localStorage.getItem('text')) {
    populateStorage();
} else {
    setText();
}

function populateStorage() {
    localStorage.setItem('text', document.getElementById('text').value);
    localStorage.setItem('font', document.getElementById('font').value);

    setText();
}
//set the text and font
function setText() {
    var currentText = localStorage.getItem('text');
    var currentFont = localStorage.getItem('font');

    document.getElementById('text').value = currentText;
    document.getElementById('font').value = currentFont;

    pElem.style.fontFamily = currentFont;
}

fontForm.onchange = populateStorage;
textForm.onchange = populateStorage;

//save the data to the server
$(document).ready(function() {
    $('#save').click(  function () {    //the save button id
        console.log("click");

        var sendData = localStorage.getItem('text', document.getElementById('text').value);
        //var sendData = $('#data').val();

        $.ajax({
            url: 'localhost',    //api url
            type: 'PUT',
            data: {
                data: sendData
            },
            success: function () {
            }
        })
        ;

    });
});