# Energy Sector Wind Turbine Assistant — GCP Gemini Enterprise POC

Multi-tool conversational AI agent on GCP for wind turbine predictive maintenance.

## Architecture
- Platform: GCP Dialogflow CX / Conversational Agents
- LLM: Gemini 2.5 Flash (Vertex AI)
- RAG: Discovery Engine Data Store (turbine manuals)
- Tools: Cloud Functions Gen2

## Tools
- turbine-knowledge-base: RAG over fault codes, maintenance schedules
- turbine-monitor: Live telemetry via Cloud Function
- workorder-tool: Work order creation via Cloud Function

## Demo Queries
1. Check the current status of turbine T-247
2. What is fault code FC-101 and how do I fix it?
3. Raise a work order for turbine T-247 fault FC-101 priority HIGH

## Author
Niranjan Babu K | Tech Mahindra Agentic AI Practice | BITS Pilani M.Tech
