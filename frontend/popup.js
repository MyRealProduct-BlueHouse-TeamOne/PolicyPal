// document.getElementById('summarizeBtn').addEventListener('click', async () => {
// 	const url = document.getElementById('urlInput').value;
// 	const response = await fetch('http://localhost:5000/summarize', {
// 		method: 'POST',
// 		headers: {
// 			'Content-Type': 'application/json',
// 		},
// 		body: JSON.stringify({ url }),
// 	});
// 	const data = await response.json();
// 	document.getElementById('summary').innerText = data.summary;
// });

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
			error.style.display='block'      
        } 
    });
    
    summaryButton.addEventListener('click', () => {
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
            chrome.tabs.sendMessage(tabs[0].id, { action: 'showSummaryCard' });
        });
        
    });

    
});
