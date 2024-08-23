import json
import re
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

with open('modified_sections.json') as f:
    dataset = json.load(f)

# Create a dictionary to map words to associated IPC sections
word_to_ipc = {}

# Preprocess the dataset to create the word_to_ipc dictionary
for entry in dataset:
    case = entry['case']
    ipc_section = entry['IPC_Section']
    
    # Tokenize the case and extract individual words
    words = re.findall(r'\b\w+\b', case.lower())
    
    # Update the word_to_ipc dictionary
    for word in words:
        if len(word) > 3:
            if word not in word_to_ipc:
                word_to_ipc[word] = set()
            word_to_ipc[word].add(ipc_section)

# Function to match user input with words from the dataset
def match_user_input(input_text):
    input_text = input_text.lower()
    input_words = re.findall(r'\b\w+\b', input_text)
    
    # Set to store matched IPC sections
    matched_sections = set()
    
    # Counter to keep track of matched words
    matched_word_count = 0
    
    # Iterate through input words and find matching IPC sections
    for word in input_words:
        if len(word) > 3 and word in word_to_ipc:
            matched_sections.update(word_to_ipc[word])
            matched_word_count += 1
    
    # If two or more words matched, return the matched IPC sections
    if matched_word_count >= 2:
        return matched_sections
    else:
        return None

@app.route('/')
def index():
    return render_template('chatbotInterface.html')

@app.route('/predict', methods=['POST'])
def predict():
    user_input = request.form.get('user_input')
    matched_sections = match_user_input(user_input)

    if matched_sections:
        return jsonify({'predicted_sections': list(matched_sections)})
    else:
        return jsonify({'predicted_sections': 'No matching IPC sections found.'})

if __name__ == '__main__':
    app.run(debug=True)
