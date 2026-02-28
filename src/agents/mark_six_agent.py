import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.utils.get_history import get_history
from src.tools.analyze_tools import *


DEFAULT_MODEL_NAME = 'x-ai/grok-beta'
load_dotenv(os.path.join('config', '.env'))

llm = ChatOpenAI(
    model=os.getenv('MODEL_NAME', DEFAULT_MODEL_NAME),
    api_key=os.getenv('OPENROUTER_API_KEY'),
    base_url=os.getenv('OPENROUTER_BASE_URL'),
    temperature=0.1,
)

class MarkSixAgent:
    def __init__(self, hist):
        self.hist = hist

    def analyze(self) -> str:
        hot_numbers_top_5 = None
        cold_numbers_top_5 = None
        for tool in mark_six_tools:
            if tool.__name__ == 'get_hot_cold_numbers':
                hot_numbers_top_5, cold_numbers_top_5 = tool(self.hist)

        user_prompt = f"""
Hot numbers: {hot_numbers_top_5}
Cold numbers: {cold_numbers_top_5}
"""
        sys_prompt = f"""
You are a Mark Six lottery analyst.
"""
        messages = [
            SystemMessage(content=sys_prompt),
            HumanMessage(content=user_prompt)
        ]
        return llm.invoke(messages).content

if __name__ == "__main__":
    hist = get_history()
    markSixAgent = MarkSixAgent(hist)
    result = markSixAgent.analyze()
    print(f"result:{result}")