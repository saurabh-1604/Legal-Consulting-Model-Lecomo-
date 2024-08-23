from flask import Flask, render_template, request, jsonify
import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

trained_input = Flask(__name__)

with open('modified_sections.json') as f:
    data = json.load(f)

texts = [entry['case'] for entry in data]
labels = [entry['IPC_Section'] for entry in data]

max_words = 1000
tokenizer = Tokenizer(num_words=max_words, oov_token='<OOV>')
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

maxlen = 100
padded_sequences = pad_sequences(sequences, maxlen=maxlen, padding='post', truncating='post')

model = load_model('ipc_section_model.keras')

with open('reverse_label_dict.json') as f:
    reverse_label_dict = json.load(f)

def predict_IPC_sections(input_text):
    # Tokenize input text
    input_sequence = tokenizer.texts_to_sequences([input_text])
    padded_input_sequence = pad_sequences(input_sequence, maxlen=maxlen, padding='post', truncating='post')
    
    # Predict IPC sections
    predictions = model.predict(padded_input_sequence)
    predicted_label_index = np.argmax(predictions)
    predicted_label = reverse_label_dict[str(predicted_label_index)]  # Convert index to string
    return predicted_label

@trained_input.route('/')
def index():
    return render_template('chatbotInterface.html')

@trained_input.route('/predict', methods=['POST'])
def predict():
    user_input = request.form['user_input']
    predicted_sections = predict_IPC_sections(user_input)
    return jsonify({'predicted_sections': predicted_sections})

if __name__ == '__main__':
    trained_input.run(debug=True)
