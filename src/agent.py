import os
from google.adk.agents import Agent


INSTRUCTION = """
You are an AI agent answering users' questions.
When providing answers, explain your understanding of the question and respond concisely and clearly
"""

root_agent = Agent(
    name = "basic_agent",
    model = "gemini-2.5-flash",
    description = "Agents that answer user questions",
    instruction = INSTRUCTION
)
