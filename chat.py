from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Assuming your 'bot_data' DataFrame is already defined
# bot_data should contain 'User_Input' and 'Bot_Response' columns

# Vectorizing the user inputs
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(bot_data['User_Input'])

def chatbot_response(user_input):
    # Transform the user input into a vector
    user_vector = vectorizer.transform([user_input.lower()])
    
    # Compute cosine similarity between the user input and stored inputs
    similarities = cosine_similarity(user_vector, vectors)

    # Find the index of the best match
    best_match_idx = similarities.argmax()

    # Return the bot's response that corresponds to the best match
    return bot_data['Bot_Response'][best_match_idx]

# Chatbot loop for continuous conversation
print("Bot: Hello! I am your assistant. Type 'exit' to end the conversation.")
while True:
    # Get user input
    user_input = input("You: ")

    # Break the loop if the user types 'exit'
    if user_input.lower() == "exit":
        print("Bot: Goodbye! Have a great day!")
        break

    # Get the bot's response
    response = chatbot_response(user_input)
    
    # Print the bot's response
    print(f"Bot: {response}")
