import json
import random
import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet

with open('cleaned_sample_dataset.json') as f:
    data = json.load(f)

# Function for synonym
def synonym_replacement(text, n=1):
    words = nltk.word_tokenize(text)
    new_words = words.copy()
    for _ in range(n):
        for i, word in enumerate(words):
            synsets = wordnet.synsets(word)
            if synsets:
                synonyms = synsets[0].lemma_names()
                if len(synonyms) > 1:
                    synonym = random.choice(synonyms)
                    new_words[i] = synonym
    return ' '.join(new_words)

# Function for random deletion
def random_deletion(text, p=0.1):
    words = nltk.word_tokenize(text)
    if len(words) == 1:
        return text
    remaining_words = [word for word in words if random.uniform(0, 1) > p]
    if len(remaining_words) == 0:
        return random.choice(words)
    return ' '.join(remaining_words)

augmented_data = []
for entry in data:
    augmented_entry = {}
    augmented_entry['case'] = entry['case']
    augmented_entry['IPC_Section'] = entry['IPC_Section']

    augmented_entry['case_synonym_replacement'] = synonym_replacement(entry['case'])
    augmented_entry['case_random_deletion'] = random_deletion(entry['case'])

    augmented_data.append(augmented_entry)

with open('augmented_dataset.json', 'w') as f:
    json.dump(augmented_data, f, indent=2)

print(json.dumps(augmented_data, indent=2))
