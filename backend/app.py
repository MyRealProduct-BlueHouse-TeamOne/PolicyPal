from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
import pandas as pd
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch  # Add torch to handle CUDA
import time

app = Flask(__name__)
CORS(app)

# Check if CUDA is available and set the device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the model and tokenizer once when the app starts
model_path = "distilbart"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path).to(device)
model.eval()  # Set the model to evaluation mode

# Move the model to the appropriate device (CPU or GPU)
model.to(device)

def scrape_terms_and_conditions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    terms_text = ' '.join([para.get_text() for para in paragraphs])
    return terms_text

def summarize_text(text, max_length=512):
    # Tokenize the input text
    # start = time.time()
    text = "Summarize the following Terms of Service in bullet points (each bullet point should be no longer than 200 characters):\n\n" + text
    inputs = tokenizer(text, max_length=1024, truncation=True, return_tensors="pt").to(device)

    # Move the inputs to the same device as the model
    inputs = {key: value.to(device) for key, value in inputs.items()}
    
    # Generate the summary
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=1024,
        min_length=50,
        length_penalty=1.0,
        num_beams=10,
        early_stopping=True
    )
    
    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    # Ensure the summary ends with proper punctuation
    last_punctuation = max(summary.rfind('.'), summary.rfind('!'), summary.rfind('?'))
    if last_punctuation != -1:
        summary = summary[:last_punctuation + 1]
    
    # end = "Time taken: " + str((time.time() - start) / 60) + "\n\n"
    return summary

@app.route('/summarize', methods=['POST'])
def summarize():
    start_time = time.time()
    
    print(f"Retreiving URL...")
    data = request.json
    url = data.get('url')
    print(f"SUCCESS: URL received. URL: {url}")
   
    # Summarization logic
    print(f"Scraping website...")
    terms_text = scrape_terms_and_conditions(url)
    print(f"SUCCESS: Website scraped. Terms text retreived.")
    
    print(f"Summarizing text...")
    summary = summarize_text(terms_text)
    print(f"SUCCESS: Terms summarized.")
    print(f"Time taken: {float(time.time() - start_time) / 60.0}")
    
    print(f"Summary generated. Type: {type(summary)}")
    print(f"Returning summary...")
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
