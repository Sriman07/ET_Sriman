# 🌐 Bharat Energy Intelligence Platform
**Sovereign Decision Support for Supply Chain Resilience**

### Overview
India imports 88% of its crude oil. When a geopolitical crisis hits, unmanaged supply shocks take an average of 47 days to stabilize, costing billions in spot premiums. The Bharat Energy Intelligence Platform is a sovereign OS that collapses that recovery gap to 6 hours. 

By utilizing a Hybrid AI architecture, the platform uses Agentic LLMs (Gemini 2.5 Flash) to ingest unstructured OSINT/geopolitical signals, and strictly offloads the procurement logic to a deterministic Operations Research solver (PuLP). Zero math hallucination. 

### Tech Stack
* **Frontend:** Streamlit, Folium (Geospatial Mapping)
* **Intelligence Core:** Gemini 2.5 Flash API
* **Mathematical Solver:** PuLP (Linear Programming)
* **Data:** Pandas, NetworkX

### How to Run Locally
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your Gemini API key to a `.env` file.
4. Execute the War Room: `streamlit run main.py`