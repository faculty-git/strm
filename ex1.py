import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

print("Key loaded:", key is not None)
print("Key prefix:", key[:8] if key else None)
print("Key length:", len(key) if key else None)

client = OpenAI(api_key=key)

response = client.responses.create(
    model="gpt-4.1-mini",
    input="Say hello"
)

print(response.output_text)
