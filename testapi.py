import openai

# Replace with your actual API key
openai.api_key = "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"

try:
    print("Sending request to OpenAI...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or whichever model you want to use
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print("Response received from OpenAI:")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
