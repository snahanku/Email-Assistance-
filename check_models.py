from google import genai
from llm_config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

models = client.models.list()

for model in models:
    print(model.name)