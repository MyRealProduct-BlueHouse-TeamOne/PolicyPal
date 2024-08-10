import requests
from bs4 import BeautifulSoup
from transformers import pipeline

# Function to scrape terms and conditions from a webpage
def scrape_terms_and_conditions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Assuming terms and conditions are within <p> tags, you might need to adjust this
    paragraphs = soup.find_all('p')
    terms_text = ' '.join([para.get_text() for para in paragraphs])
    return terms_text

# Function to split text into chunks of a specified max length
def split_text(text, max_length):
    words = text.split()
    for i in range(0, len(words), max_length):
        yield ' '.join(words[i:i + max_length])

# Function to summarize text using a pre-trained language model
def summarize_text(text, max_length=512):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    chunks = list(split_text(text, max_length))
    summaries = [summarizer(chunk, max_length=200, min_length=50, do_sample=False)[0]['summary_text'] for chunk in chunks]
    return ' '.join(summaries)

# Main function to scrape and summarize
def main():
    url = input("Enter the URL of the terms and conditions page: ")
    terms_text = scrape_terms_and_conditions(url)
    
    if terms_text:
        print("Scraped terms and conditions successfully.")
        print("Summarizing...")
        summary = summarize_text(terms_text)
        print("Summary:")
        print(summary)
    else:
        print("Failed to scrape terms and conditions.")

if __name__ == "__main__":
    main()
