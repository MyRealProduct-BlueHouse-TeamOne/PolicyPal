document.getElementById('summarizeBtn').addEventListener('click', async () => {
	const url = document.getElementById('urlInput').value;
	const response = await fetch('http://localhost:5000/summarize', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ url }),
	});
	const data = await response.json();
	document.getElementById('summary').innerText = data.summary;
});
