import pulp
import pandas as pd

def run_optimization_engine(risk_assessment):
    """
    Takes the risk parameters from Agent 1 (LLM) and runs a deterministic 
    Linear Programming solver to find the optimal crude routing strategy.
    """
    print("\nAgent 3: Initializing Operations Research Mathematical Solver...")

    # Integrated 'Strategic_Petroleum_Reserve' as an emergency nodal asset
    suppliers = {
        'Iraq': {'capacity': 1.2, 'base_price': 80.0},
        'Russia': {'capacity': 1.5, 'base_price': 75.0}, 
        'Saudi_Arabia': {'capacity': 1.0, 'base_price': 85.0},
        'West_Africa': {'capacity': 0.8, 'base_price': 82.0},
        'USA': {'capacity': 0.6, 'base_price': 83.0},
        'Strategic_Petroleum_Reserve': {'capacity': 4.5, 'base_price': 130.0} 
    }
    
    national_demand = 4.5 
    
    shipping_routes = {
        ('Iraq', 'Strait of Hormuz'): {'cost': 2.0, 'capacity': 2.0},
        ('Saudi_Arabia', 'Strait of Hormuz'): {'cost': 2.0, 'capacity': 2.0},
        ('Russia', 'Red Sea'): {'cost': 3.5, 'capacity': 1.8},
        ('West_Africa', 'Cape of Good Hope'): {'cost': 4.5, 'capacity': 1.5},
        ('USA', 'Cape of Good Hope'): {'cost': 5.0, 'capacity': 1.5},
        ('Strategic_Petroleum_Reserve', 'Strategic Drawdown'): {'cost': 0.0, 'capacity': 4.5}
    }

    # 2. APPLY AI RISK CONSTRAINTS
    target_corridor = "Strait of Hormuz"
    capacity_lost = risk_assessment.get('capacity_reduction_estimate', 0)
    risk_score = risk_assessment.get('risk_score', 0)
    
    if capacity_lost > 0:
        print(f">> Math Engine: Applying {capacity_lost*100}% capacity constraint to {target_corridor}")
        for (supplier, corridor), data in shipping_routes.items():
            if corridor == target_corridor:
                data['capacity'] = data['capacity'] * (1 - capacity_lost)
                data['cost'] = data['cost'] + (risk_score * 0.05) 

    # 3. DEFINE LINEAR PROGRAMMING PROBLEM
    prob = pulp.LpProblem("Crude_Supply_Optimization", pulp.LpMinimize)
    route_vars = pulp.LpVariable.dicts("Route", shipping_routes.keys(), lowBound=0, cat='Continuous')

    # Objective Function
    prob += pulp.lpSum([route_vars[(sup, cor)] * (suppliers[sup]['base_price'] + shipping_routes[(sup, cor)]['cost']) 
                        for (sup, cor) in shipping_routes.keys()])

    # Constraints
    prob += pulp.lpSum([route_vars[(sup, cor)] for (sup, cor) in shipping_routes.keys()]) == national_demand, "Meet_National_Demand"

    for sup in suppliers.keys():
        prob += pulp.lpSum([route_vars[(s, c)] for (s, c) in shipping_routes.keys() if s == sup]) <= suppliers[sup]['capacity'], f"Max_Cap_{sup}"

    for (sup, cor), data in shipping_routes.items():
        prob += route_vars[(sup, cor)] <= data['capacity'], f"Corridor_Cap_{sup}_{cor}"

    #4. SOLVE
    prob.solve(pulp.PULP_CBC_CMD(msg=0))

    #5. FORMAT OUTPUT
    optimal_routes = []
    total_cost = pulp.value(prob.objective)
    
    # Calculate unmanaged baseline cost
    unmanaged_cost = total_cost + (risk_score * 0.8) if capacity_lost > 0 else total_cost
    savings = unmanaged_cost - total_cost
    
    for v in prob.variables():
        if v.varValue > 0.01:
            clean_name = v.name.replace("Route_('", "").replace("',_'", " via ").replace("')", "")
            optimal_routes.append({
                "path": clean_name,
                "volume_mbpd": round(v.varValue, 2)
            })
            
    # Check if SPR was utilized
    status_msg = "Optimal Solution Found"
    for r in optimal_routes:
        if "Strategic_Petroleum_Reserve" in r["path"]:
            status_msg = "Supply Deficit: Active SPR Drawdown Mandated"

    return {
        "status": status_msg,
        "total_daily_cost_millions": round(total_cost, 2),
        "unmanaged_cost_millions": round(unmanaged_cost, 2),
        "optimization_savings_millions": round(savings, 2),
        "rerouting_plan": optimal_routes
    }
