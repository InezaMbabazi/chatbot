import nltk
import pandas as pd
from nltk.tokenize import word_tokenize

# Set the NLTK data path
nltk.data.path.append('./.nltk_data')  # Adjust this path if necessary

# Function to preprocess text
def preprocess_text(text):
    # Tokenize the text into words
    tokens = word_tokenize(text.lower())
    # Add more preprocessing steps as needed (e.g., removing punctuation, stopwords, etc.)
    return tokens

# Load your DataFrame
df = pd.read_csv('Chatbot.csv')

# Check if 'Questions' column exists
if 'Questions' in df.columns:
    # Process the 'Questions' column
    df['Processed_Questions'] = df['Questions'].apply(preprocess_text)
else:
    print("The 'Questions' column is not found in the DataFrame.")

# Example of using the processed data (you can modify this part as needed)
# For instance, you can print the first few rows of the DataFrame
print(df[['Questions', 'Processed_Questions']].head())

# You can add more functionality below to build your chatbot
# For example, implementing the chatbot response logic, etc.
