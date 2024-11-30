const btn = document.getElementById("summarise");
btn.addEventListener("click", function() {
    btn.disabled = true;
    btn.innerHTML = "Summarising...";
    
    // Get the current active tab URL
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        var url = tabs[0].url;
        
        // Make the GET request to Flask server
        var xhr = new XMLHttpRequest();
        xhr.open("GET", "http://127.0.0.1:5000/summary?url=https://youtu.be/nyhRNwTfydU?si=f39AMKnLEP8hPwa7" + encodeURIComponent(url), true);
        
        // Handle the server's response
        xhr.onload = function() {
            if (xhr.status === 200) {
                var text = xhr.responseText;
                const p = document.getElementById("output");
                p.innerHTML = text;  // Show the summary
            } else {
                const p = document.getElementById("output");
                p.innerHTML = "Error: " + xhr.responseText;  // Display error message
            }
            
            // Enable the button after the request is completed
            btn.disabled = false;
            btn.innerHTML = "Summarise";
        };
        
        xhr.onerror = function() {
            const p = document.getElementById("output");
            p.innerHTML = "Request failed. Please check if the server is running.";
            btn.disabled = false;
            btn.innerHTML = "Summarise";
        };

        xhr.send();
    });
});
