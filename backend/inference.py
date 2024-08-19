from bs4 import BeautifulSoup
import requests
import pandas as pd
from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments, AutoModelForSeq2SeqLM, AutoTokenizer
import time

# Load the model and tokenizer once when the app starts
model_path = "distilbart"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
model.eval()  # Set the model to evaluation mode


def scrape_terms_and_conditions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    paragraphs = soup.find_all('p')
    terms_text = ' '.join([para.get_text() for para in paragraphs])
    return terms_text


def summarize_text(text, max_length=512):
    # Tokenize the input text
    start = time.time()
    text = "Summarize the following Terms of Service in bullet points so that each point is around 30 words max:\n\n"+text
    print(text)
    print(len(text))
    inputs = tokenizer(text, max_length=1024, truncation=True, return_tensors="pt")
    
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
    
    end = "Time taken: "+ str((time.time() - start)/60) + "\n\n"
    return end+summary


def main():
    url = "https://www.dropbox.com/terms"
    # Summarization logic
    terms_text = scrape_terms_and_conditions(url)
    summary = summarize_text(terms_text)
    print(summary)

if __name__ == "__main__":
    main()