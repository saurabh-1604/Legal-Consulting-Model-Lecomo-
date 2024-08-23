import json
import re
import string
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords

with open('modified_sections.json') as f:
    data = json.load(f)

def clean_text(text):
    # Remove special characters and punctuation
    text = re.sub(r'[^\w\s]', '', text)
    # Convert text to lowercase
    text = text.lower()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = nltk.word_tokenize(text)
    filtered_words = [word for word in words if word not in stop_words]
    # Join filtered words back into text
    cleaned_text = ' '.join(filtered_words)
    return cleaned_text

cleaned_data = []
for entry in data:
    cleaned_entry = {}
    cleaned_entry['case'] = clean_text(entry['case'])
    cleaned_entry['IPC_Section'] = entry['IPC_Section']
    cleaned_data.append(cleaned_entry)

output_file = 'cleaned_sample_dataset.json'
with open(output_file, 'w') as f:
    json.dump(cleaned_data, f, indent=2)

print(f"Cleaned dataset saved to {output_file}")
