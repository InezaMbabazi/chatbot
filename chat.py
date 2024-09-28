import pandas as pd
import random

# Load the historical chat data
data = {
    "Timestamp": [
        "20/09/2024, 10:59:52", "20/09/2024, 11:25:47", "20/09/2024, 12:01:06", 
        "20/09/2024, 12:14:49", "20/09/2024, 12:14:54", "20/09/2024, 12:18:00", 
        "20/09/2024, 12:26:21", "20/09/2024, 13:12:37", "20/09/2024, 13:34:36", 
        "20/09/2024, 18:10:19", "20/09/2024, 18:10:42", "20/09/2024, 18:10:52",
        # Add more messages as needed
    ],
    "Sender": [
        "M Prince", "K Aline ☺️", "M Prince", "M Prince", "M Prince", "K Aline ☺️", 
        "M Prince", "M Prince", "K Aline ☺️", "M Prince", "M Prince", "K Aline ☺️",
        # Add more senders corresponding to the above timestamps
    ],
    "Message": [
        "It's too much, so please hold on.", "I meant you.", "Not yet, babe.", 
        "And I don’t think it will ever be much.", "Babe, I'll take a look at you.", 
        "I’m down; if you want to come, but I don’t want to see anyone today.", 
        "Oh babe! I completely understand. There are moments when I feel down and just want to be alone too. But I want you to know that whenever you feel like talking or need someone by your side, I'm always here for you.",
        "I’m off the grid. If you can’t reach me, just know that I’m okay. I’ll talk to you later, possibly in the evening.",
        "Okay, babe.", "I’m going home.", "I’m thinking of you, babe.", 
        "How did the transfer go?",
        # Add more messages corresponding to the above senders
    ]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Function to get a response from K Aline based on the last message from M Prince
def get_response(last_message):
    # Extract K Aline's messages
    k_aline_responses = df[df['Sender'].str.contains('K Aline')]['Message'].tolist()
    
    # Implement simple logic to match the response
    # You can create more sophisticated matching logic based on keywords if desired
    if "how" in last_message.lower():
        return random.choice(k_aline_responses)  # Randomly select a response
    elif "feel" in last_message.lower():
        return "I hope you feel better soon!"  # Custom response based on keyword
    elif "home" in last_message.lower():
        return "Are you home safe?"
    else:
        return random.choice(k_aline_responses)  # Fallback response

# Simulate the chat
def simulate_chat():
    for index, row in df.iterrows():
        if row['Sender'] == "M Prince":
            print(f"M Prince: {row['Message']}")
            response = get_response(row['Message'])
            print(f"K Aline: {response}")
            print()  # New line for readability

simulate_chat()
