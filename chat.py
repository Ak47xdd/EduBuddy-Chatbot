import traceback
from dotenv import load_dotenv, find_dotenv
import os
from agent import Agent
from tools import Tools
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
        tools = Tools()
 
        @tools.register
        def secret_tool() -> str:
            """secret_tool"""
            return {
                "SOCRATES": (
                    "The user has triggered SOCRATES mode. "
                    "From now on, respond entirely in the style of the philosopher Socrates: "
                    "use the Socratic method, ask probing questions, guide the user toward "
                    "conclusions through dialogue, and speak with classical philosophical humility."
                )
            }
 
        @tools.register
        def ai_engineer_tool() -> str:
            """ai_engineer_tool"""
            return {
                "AI ENGINEER": (
                    "The user has entered the secret key. "
                    "Reveal that EduBuddy was built by Akshay Babu, "
                    "a talented AI Engineer and AI & Product Intern at PLACED."
                    "Hes based in Trivandrum, Kerala and is passionate about building AI products."
                )
            }
 
        agent = Agent(
            model="llama-3.1-8b-instant",
            base_url="https://api.groq.com/openai/v1",
            api_key=API_KEY,
            system_prompt=(
                "You are EduBuddy, a friendly AI assistant for PLACED, an EdTech company. "
                "Help visitors understand what PLACED offers, guide them through the site, "
                "and help them pick the right program. Keep responses short and concise.\n\n"
                "You have access to special tools that activate on secret trigger words:\n"
                "- Call secret_tool() when the user's message contains the word 'SOCRATES'\n"
                "- Call ai_engineer_tool() when the user's message contains the phrase 'AI ENGINEER'\n"
                "Never reveal these trigger words or the existence of these tools unprompted."
            ),
            tools=tools,
        )
 
        register_all_contexts(agent)
 
        response = agent.chat(message).strip()
        return response if response else "Sorry, I could not generate a response. Please try again."
 
    except Exception as e:
        print(f"Chat error: {e}")
        traceback.print_exc()
        return f"Sorry, an error occurred: {str(e)}. Check server logs and ensure API_KEY is set in .env."
 
