import nltk
import pandas as pd
from nltk.tokenize import word_tokenize

# Set the NLTK data path
nltk.data.path.append('./.nltk_data')  # Adjust this path if necessary

# Try to download the punkt tokenizer if it's not available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Punkt tokenizer not found. Downloading...")
    nltk.download('punkt')

# Function to preprocess text
def preprocess_text(text):
    try:
        # Tokenize the text into words
        tokens = word_tokenize(text.lower())
        return tokens
    except LookupError as e:
        print(f"Error in tokenizing text: {e}")
        return []

# Load your DataFrame
df = pd.read_csv('Chatbot.csv')

# Check if 'Questions' column exists
if 'Questions' in df.columns:
    # Process the 'Questions' column
    df['Processed_Questions'] = df['Questions'].apply(preprocess_text)
else:
    print("The 'Questions' column is not found in the DataFrame.")

# Example of using the processed data (you can modify this part as needed)
print(df[['Questions', 'Processed_Questions']].head())

# Additional chatbot functionality goes here...
