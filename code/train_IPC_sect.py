import json
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Conv1D, MaxPooling1D, Flatten

with open('augmented_dataset.json') as f:
    data = json.load(f)

texts = [entry['case'] for entry in data]
labels = [entry['IPC_Section'] for entry in data]

# Tokenize texts
max_words = 1000
tokenizer = Tokenizer(num_words=max_words, oov_token='<OOV>')
tokenizer.fit_on_texts(texts)
sequences = tokenizer.texts_to_sequences(texts)

maxlen = 100
padded_sequences = pad_sequences(sequences, maxlen=maxlen, padding='post', truncating='post')

label_dict = {label: i for i, label in enumerate(set(labels))}
reverse_label_dict = {i: label for label, i in label_dict.items()}
labels_encoded = np.array([label_dict[label] for label in labels])

# Define model
model = Sequential([
    Embedding(max_words, 32), #Embedding(max_words, 32, input_length=maxlen),
    Conv1D(64, 5, activation='relu'),
    LSTM(64, dropout=0.2, recurrent_dropout=0.2),
    Dense(64, activation='relu'),
    Dense(len(label_dict), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(padded_sequences, labels_encoded, epochs=500, validation_split=0.2)

model.save('ipc_section_model.keras')

with open('reverse_label_dict.json', 'w') as f:
    json.dump(reverse_label_dict, f)
