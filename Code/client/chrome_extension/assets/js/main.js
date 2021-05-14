const params = new URLSearchParams(window.location.search);
//window.onload = function() {

var button1 = document.getElementById("button1")
    //button1.setAttribute('href', params.get('blocked'))
button1.addEventListener('click', function() {
    console.log("Sending Message");
    //chrome.runtime.sendMessage(params.get('id'), { URL: params.get('blocked') });
    chrome.runtime.sendMessage({ URL: params.get('blocked'), message: "whitelist" });
    //window.location.replace(params.get('blocked'));
    location.replace(params.get('blocked'));

});

var button2 = document.getElementById("button2");
button2.addEventListener('click', function() {
    history.go(-2);
})


//}