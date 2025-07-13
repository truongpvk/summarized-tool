import google
from google import genai
from google.genai import types
import json
import re
import dotenv
import os

dotenv.load_dotenv("../..")

def get_response(
  context: str, 
  client=genai.Client(api_key="AIzaSyC3ASGq0nHXZqOBNSCzBZXYk0BuafvDlBQ"), 
  model='gemini-2.5-flash-lite-preview-06-17', 
  temperature=0.1, 
  thinking=True, 
  instruction: str=None
):
    if not context:
      return None
    
    config = types.GenerateContentConfig()
    config.temperature = temperature
    if not thinking:
      config.thinking_config = types.ThinkingConfig(thinking_budget=0)
    
    if instruction:
      config.system_instruction = instruction
    
    
    response = client.models.generate_content(
      model=model,
      contents=context,
      config=config
    )
    
    return response.text

def create_prompt(text: str):
  return "Summarize: " + text + "Just return the summary paragraph in the same language of input paragraph."

