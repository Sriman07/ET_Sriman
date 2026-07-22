from agents.agent1_risk import run_risk_agent
from agents.agent2_simulator import run_scenario_modeller
from agents.agent3_optimization import run_optimization_engine
from agents.agent4_executive import run_executive_advisor

if __name__ == "__main__":
    print("=== INITIATING NATIONAL ENERGY WAR ROOM PIPELINE (STRATEGY 3) ===")
    
    # 1. Agent 1: Geopolitical Risk Ingestion
    risk_assessment = run_risk_agent('data/scenario_1.json')
    
    if risk_assessment:
        print(f">> Agent 1 Complete. Risk Score: {risk_assessment['risk_score']}/100")
        
        # 2. Agent 2: Macroeconomic & Refinery Simulation
        simulation_data = run_scenario_modeller(risk_assessment)
        print(f">> Agent 2 Complete. Vulnerability Tier: {simulation_data['systemic_risk_metric']}")
        
        # 3. Agent 3: Pure Operations Research Optimization
        optimal_plan = run_optimization_engine(risk_assessment)
        print(f">> Agent 3 Complete. Solved Daily Cost: ${optimal_plan['total_daily_cost_millions']}M")
        
        # 4. Agent 4: Executive Synthesis
        final_brief = run_executive_advisor(risk_assessment, simulation_data, optimal_plan)
        
        print("\n==================================================")
        print("=== BHARAT ENERGY RESILIENCE WAR ROOM OUTPUT ===")
        print("==================================================")
        print(f"SYSTEM CONFIDENCE SCORE: {final_brief['confidence_score']}%")
        print(f"NATIONAL SECURITY VULNERABILITY: {simulation_data['systemic_risk_metric']}")
        print(f"\nCRITICAL MANDATE:\n{final_brief['executive_directive']}")
        
        print(f"\nMACRO IMPACT FORECAST:")
        print(f"- Retail Price Shock:   +₹{simulation_data['retail_fuel_delta_inr']} per liter")
        print(f"- National GDP Drag:     -{simulation_data['gdp_drag_percent']}%")
        print(f"- Refinery Operational Profile: {simulation_data['refinery_stress_profile']}")
        
        print("\nMATHEMATICAL REROUTING DISPATCH LOGS:")
        for route in optimal_plan['rerouting_plan']:
            print(f"  -> Dispatching {route['volume_mbpd']} MBPD via {route['path']}")
            
        print("\nACTION TIMELINE DEPLOYMENT MATRIX:")
        print(f"  [T + 06H]: {final_brief['action_timeline']['next_6_hours']}")
        print(f"  [T + 24H]: {final_brief['action_timeline']['next_24_hours']}")
        print(f"  [T + 48H]: {final_brief['action_timeline']['next_48_hours']}")
        print("==================================================")