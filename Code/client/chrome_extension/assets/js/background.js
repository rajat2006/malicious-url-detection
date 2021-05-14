// var x = 0
// chrome.runtime.onMessage.addListener(function(request, sender){
//     console.log("hi", x);
//     if(x==1){
//     chrome.tabs.update(sender.tab.id, {url:request.redirect});
//     x = 1;
//     }

// });

async function check_url_list(URL) {
    var promise = new Promise(function(resolve, reject) {
        chrome.storage.sync.get(['whitelist'], function(result) {
            resolve(result['whitelist'])

        })
    });

    const value = await promise;
    if (value != undefined) {
        var val = Object.values(value);
        return val.some((url) => url == URL);
    }
    return false;

}

chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {

    if (changeInfo.hasOwnProperty('url') &&
        /^(https?|file):/.test(changeInfo.url)) {

        var URL = changeInfo.url;
        console.log("URL - ", URL);
        check_url_list(URL)
            .then((found) => {
                if (found) {
                    console.log("Benign", "Local");
                } else {
                    $.ajax({
                        type: 'POST',
                        contentType: "application/json",
                        url: "http://127.0.0.1:5000/",
                        data: JSON.stringify(URL),
                        datatype: "json",
                        success: function(response) {
                            if (response == 1) {
                                console.log("Response:", "Malicious", "Server");
                                // not working //chrome.tabs.sendMessage(tabId, { greeting: "hello" });
                                //chrome.tabs.update(sender.tab.id, {url:request.redirect});
                                var redirect_url = chrome.runtime.getURL("malicious_page.html") + "?blocked=" + encodeURIComponent(URL);
                                chrome.tabs.update(tabId, { url: redirect_url });

                            } else
                                console.log("Response:", "Benign", "Server");
                        }
                    });
                }

            });
    }
    return true;
});

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    console.log("Message Received");
    chrome.storage.sync.get(["whitelist"], function(result) {
        var array = result["whitelist"] ? result["whitelist"] : [];
        const found = array.find(url => url == request.URL);
        if (found == undefined) {
            array.push(request.URL);
            chrome.storage.sync.set({ "whitelist": array });
            console.log("Added to Local List");
        }
    })
});