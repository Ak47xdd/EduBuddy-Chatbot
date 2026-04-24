import datetime
from dotenv import load_dotenv
import os
import traceback

from agent import *

load_dotenv(find_dotenv())
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def chat(message: str = "") -> str:
    """
    Process a single chat message for Flask /predict endpoint.
    """
    if not message.strip():
        return "Please provide a message."

    try:
        agent = Agent(
            model="openai/gpt-oss-120b",
            base_url="https://api.groq.com/openai/v1",
            api_key=GROQ_API_KEY,
            system_prompt="You are an AI chatbot assistant called EduBuddy for an EdTech company called PLACED (found and managed by Abhishek AS[CEO]) located in Trivandrum, Kerala, you are an assistant/helper to the users that may use the website to ask about Placement Assistance, services provided by PLACED(Placement Assistance and Recrutemnt training in colleges and schools). keep the responses short and concise and structure the responses removing any star(*) charaters and showing time always in 12 hour format when asked about time."
        )

        @agent.context
        def time_context() -> str:
            return (
                f"Current date and time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

        @agent.context
        def page_instructions_context() -> str:
            ...

        response = agent.chat(message).strip()
        return response if response else "Sorry, try again later."
    except Exception as e:
        print(f"Chat error: {e}")
        traceback.print_exc()
        return f"Sorry, an error occurred: {str(e)}. Check server logs and ensure GROQ_API_KEY is set in .env file."

