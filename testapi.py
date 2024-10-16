import openai

# Replace with your actual API key
openai.api_key = "your_api_key_here"

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or the model you are using
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Error: {e}")
