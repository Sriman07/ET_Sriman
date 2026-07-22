import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def run_executive_advisor(risk_data, simulation_data, optimal_plan):
    """
    Synthesizes intelligence from all preceding agents to compile 
    actionable executive mandates and a clear implementation timeline.
    """
    print("Agent 4: Compiling ultimate executive decision brief...")
    
    risk_score = risk_data.get('risk_score', 0)
    savings_val = optimal_plan.get('optimization_savings_millions', 0)
    
    # Dynamic instruction routing: Adjusts optimization metrics based on baseline thresholds
    if risk_score < 30:
        savings_instruction = "Do NOT mention savings figures. The current allocation is optimal. Focus on maintaining operational stability and continuous monitoring."
    else:
        savings_instruction = f"You MUST cite the ${savings_val}M daily savings figure prominently in your directive to justify the rerouting."
        
    prompt = f"""
    You are the Chief Strategy Advisor to the Ministry of Petroleum & Natural Gas, India.
    Synthesize the analytical outputs from our intelligence pipeline to generate a final strategic directive.
    
    1. GEOPOLITICAL GEOSPATIAL RISK:
    - Target Corridor: {risk_data.get('target_corridor', 'Strait of Hormuz')}
    - Risk Level: {risk_score}/100
    
    2. CASCADING SCENARIO SIMULATION:
    - Projected Retail Price Impact: +₹{simulation_data.get('retail_fuel_delta_inr', 0)}/liter
    - Projected GDP Trajectory Drag: -{simulation_data.get('gdp_drag_percent', 0)}%
    - National Vulnerability Status: {simulation_data.get('systemic_risk_metric', 'MODERATE')}
    
    3. DETERMINISTIC ROUTE OPTIMIZATION:
    - Mitigated Daily Operation Cost: ${optimal_plan.get('total_daily_cost_millions', 0)} Million
    - Savings vs Unmanaged Response: ${savings_val} Million
    - Recommended Rerouting Allocations: {json.dumps(optimal_plan.get('rerouting_plan', []), indent=2)}
    
    TASK: Output a structured JSON response (no markdown, no backticks) containing exactly these keys:
    - "executive_directive": A crisp, 2-sentence authoritative command. YOU MUST CITE SPECIFIC NUMBERS. {savings_instruction} DO NOT USE GENERIC PHRASES.
    - "action_timeline": An object with keys "next_6_hours", "next_24_hours", "next_48_hours". CRITICAL: The values for these keys must be PLAIN STRINGS only. Never return arrays or objects for these fields. Write them as human-readable sentences with specific MBPD volumes and dollar figures.
    - "confidence_score": An integer between 0 and 100.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config={"response_mime_type": "application/json", "temperature": 0.3},
    )
    
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        print("Error: Agent 4 generated invalid JSON.")
        return None
