import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def run_scenario_modeller(risk_assessment):
    """
    Computes cascading macroeconomic impacts and refinery stress profiles
    based on the risk metrics provided by Agent 1.
    """
    print("Agent 2: Simulating macroeconomic impacts and refinery stress...")
    
    capacity_lost = risk_assessment.get('capacity_reduction_estimate', 0)
    risk_score = risk_assessment.get('risk_score', 0)
    
    # 1. Deterministic Macro Modeling Math
    # Baseline assumption: Normal daily procurement cost inflation delta
    cost_variance_multiplier = risk_score * capacity_lost
    
    retail_fuel_delta_inr = round(max(0, cost_variance_multiplier * 0.25), 2)
    gdp_drag_percent = round(max(0, cost_variance_multiplier * 0.005), 3)
    
    # 2. LLM Contextual Simulator
    # Use Gemini to predict specific infrastructural stress points across Indian refineries
    prompt = f"""
    You are an advanced economic simulation engine for critical national infrastructure.
    A supply disruption has occurred at the Strait of Hormuz.
    - Risk Severity: {risk_score}/100
    - Estimated Capacity Lost: {capacity_lost * 100}%
    
    Simulate the operational impact on major Indian refining complexes (e.g., Jamnagar, Paradip, Vadinar).
    Output a pure JSON object (no markdown, no backticks) with exactly these two keys:
    - "refinery_stress_profile": A brief 1-sentence breakdown of which refineries face immediate crude grade mismatch or run-rate issues.
    - "systemic_risk_metric": A string rating ("LOW", "MODERATE", "HIGH", "CRITICAL") representing national grid vulnerability.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config={"response_mime_type": "application/json", "temperature": 0.2},
    )
    
    try:
        sim_context = json.loads(response.text)
        
        # Merge the deterministic math with the generative infrastructure simulation
        return {
            "retail_fuel_delta_inr": retail_fuel_delta_inr,
            "gdp_drag_percent": gdp_drag_percent,
            "refinery_stress_profile": sim_context["refinery_stress_profile"],
            "systemic_risk_metric": sim_context["systemic_risk_metric"]
        }
    except json.JSONDecodeError:
        print("Error: Agent 2 generated invalid JSON.")
        return None
