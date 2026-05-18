import traceback
from dotenv import load_dotenv, find_dotenv
import os
from agent import Agent
from context import register_all_contexts
 
load_dotenv(find_dotenv())
API_KEY = os.getenv("API_KEY")
 
def chat(message: str = "") -> str:
    """
    Process a single chat message for the FastAPI /predict endpoint.
    """
    if not message.strip():
        return "Please provide a message."
 
    try:
        agent = Agent(
            model="llama-3.1-8b-instant",
            base_url="https://api.groq.com/openai/v1",
            api_key=API_KEY,
            system_prompt=(
                "You are EduBuddy, a friendly AI assistant for PLACED, an EdTech company. "
                "Help visitors understand what PLACED offers, guide them through the site, "
                "and help them pick the right program. Keep responses short and concise."
            ),
        )
 
        # Loads all PLACED knowledge from placed_kb.json (or static fallback)
        register_all_contexts(agent)
 
        response = agent.chat(message).strip()
        return response if response else "Sorry, I could not generate a response. Please try again."
 
    except Exception as e:
        print(f"Chat error: {e}")
        traceback.print_exc()
        return f"Sorry, an error occurred: {str(e)}. Check server logs and ensure API_KEY is set in .env."
