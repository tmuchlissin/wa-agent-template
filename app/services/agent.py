from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

def init_agent(model, system_instruction):
    agent = create_agent(
        model=model,
        system_prompt=system_instruction,
        tools=[],
        checkpointer=InMemorySaver()
    )
    return agent
