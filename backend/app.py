from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    url = data.get('url', '')
   
    # Summarization logic goes here
    
    return jsonify({'summary': 'Summary will appear here'})

if __name__ == '__main__':
    app.run(debug=True)
