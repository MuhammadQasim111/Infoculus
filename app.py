import streamlit as st
from newsapi import NewsApiClient
from groq import AsyncGroq
from config.config import GROQ_API_KEY, NEWS_API_KEY
from agent.orchestrator import AgentOrchestrator
import asyncio

# Initialize clients
groq_client = AsyncGroq(api_key=GROQ_API_KEY)
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# Initialize AgentOrchestrator with the client
orchestrator = AgentOrchestrator(groq_client)

st.title("AI Agents: Shaitani Calculator & Newscaster Agent")

query = st.text_input("Enter your query below:", key="query")

if query:
    st.info("Processing your query...")
    
    try:
        # Create a placeholder for streaming output
        output_placeholder = st.empty()
        full_response = []
        
        # Process the async generator
        async def process_stream():
            async for chunk in orchestrator.route_query(query):
                full_response.append(chunk)
                # Update the placeholder with accumulated response
                output_placeholder.markdown("".join(full_response))
        
        # Run the async function
        asyncio.run(process_stream())
        st.success("Query processed!")
    except Exception as e:
        st.error(f"An error occurred: {e}")