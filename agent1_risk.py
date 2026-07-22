import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

# Initialize the Gemini Client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def run_risk_agent(scenario_file_path):
    """Reads unstructured intel and outputs a structured risk assessment."""
    print("Agent 1: Ingesting intelligence feeds...")
    
    # 1. Load the mock data
    with open(scenario_file_path, 'r') as file:
        raw_data = json.load(file)
        
    signals_text = "\n".join(raw_data['signals'])
    corridor = raw_data['target_corridor']
    
    # 2. Craft the Executive Prompt
    prompt = f"""
    You are an elite geopolitical risk analyst for the Indian Ministry of Petroleum.
    Review the following real-time intelligence signals regarding the {corridor}:
    
    SIGNALS:
    {signals_text}
    
    Your task is to assess the threat level and output a pure JSON object (no markdown, no backticks).
    The JSON must have the following keys exactly:
    - "risk_score": an integer from 0 to 100 representing disruption probability.
    - "confidence": an integer from 0 to 100 representing data reliability.
    - "capacity_reduction_estimate": a float between 0.0 and 1.0 (e.g., 0.5 means 50% capacity lost).
    - "executive_summary": a 2-sentence summary of the threat.
    """
    
    # 3. Call Gemini (Using Flash for speed and massive context)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json", # Forces strict JSON output
            temperature=0.2 # Low temperature for analytical consistency
        ),
    )
    
    # 4. Parse and return the JSON
    try:
        risk_assessment = json.loads(response.text)
        return risk_assessment
    except json.JSONDecodeError:
        print("Error: Gemini returned invalid JSON.")
        print("Raw output:", response.text)
        return None