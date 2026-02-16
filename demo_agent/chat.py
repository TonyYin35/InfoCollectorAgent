"""
LangGraph Demo Chat Agent
Run:  python chat.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("Error: Set GOOGLE_API_KEY in a .env file or as an env variable.")
    raise SystemExit(1)

from agent import build_agent

THREAD_ID = "demo-thread-1"


def main():
    agent = build_agent()
    config = {"configurable": {"thread_id": THREAD_ID}}

    print("=== LangGraph Chat Agent ===")
    print("Tools: get_current_time, calculate, search_info")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
        )

        ai_message = result["messages"][-1]
        print(f"Agent: {ai_message.content}\n")


if __name__ == "__main__":
    main()
