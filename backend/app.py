from flask import Flask, request, jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
import requests
from transformers import pipeline

app = Flask(__name__)
CORS(app)

def scrape_terms_and_conditions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    terms_text = ' '.join([para.get_text() for para in paragraphs])
    return terms_text

def split_text(text, max_length):
    words = text.split()
    for i in range(0, len(words), max_length):
        yield ' '.join(words[i:i + max_length])

def summarize_text(text, max_length=512):
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn')
    chunks = list(split_text(text, max_length))
    summaries = [summarizer(chunk, max_length=200, min_length=50, do_sample=False)[0]['summary_text'] for chunk in chunks]
    return ' '.join(summaries)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    url = data.get('url')
   
    # Summarization logic goes here
    terms_text = scrape_terms_and_conditions(url)
    summary = summarize_text(terms_text)
    
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
