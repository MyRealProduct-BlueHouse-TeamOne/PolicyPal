
document.addEventListener('DOMContentLoaded', () => {
    
   
    const summaryButton = document.getElementById('summary-button');
    const error = document.getElementById('noTCs');

    const urlPatterns = ["*://*/*terms*",
          "*://*/*services*",
          "*://*/*conditions*",
          "*://*/*policy*",
          "*://*/*policies*",
          "*://*/*legal*",
          "*://*/*disclaimer*",
          "*://*/*privacy*",
          "*://*/*agreement*",
          "*://*/*notice*",
          "*://*/*compliance*",
          "*://*/*contract*",
          "*://*/*regulation*",
          "*://*/*rights*"];

    // Get the current tab's URL
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        const currentUrl = tabs[0].url;

        // Check if the current URL matches any of the defined patterns
        const matchesPattern = urlPatterns.some(pattern => {
            const regex = new RegExp(pattern.replace(/\*/g, '.*'));
            return regex.test(currentUrl);
        });

        // Apply styling based on whether the URL matches the pattern
        if (!matchesPattern) {
            summaryButton.style.display = 'none';
            error.style.display='block';
        }

        // **New code to send URL to back-end and trigger content script**
        summaryButton.addEventListener('click', () => {
            //Testing calling API directly in content JS. This lets you switch tabs and generate multiple summaries at once
            chrome.tabs.sendMessage(tabs[0].id, { action: 'showSummaryCard'});
            
            // Send the URL to the back-end
            // fetch('http://localhost:5000/summarize', {
            //     method: 'POST',
            //     headers: {
            //         'Content-Type': 'application/json',
            //     },
            //     body: JSON.stringify({ url: currentUrl }),
            // })
            // .then(response => response.json())
            // .then(data => {
            //     // Send the summary to the content script
            //     chrome.tabs.sendMessage(tabs[0].id, { action: 'showSummaryCard', summary: data.summary });
            // })
            // .catch(error => {
            //     console.error('Error:', error);
            //     alert('Failed to summarize the page.');
            // });
        });
    });
});
