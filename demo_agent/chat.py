"""
LangGraph Demo Chat Agent
Run:  python chat.py
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from langchain_core.messages import AIMessageChunk
from agent import build_agent

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    print("Error: Set GOOGLE_API_KEY in a .env file or as an env variable.")
    raise SystemExit(1)


THREAD_ID = "demo-thread-1"


async def main():
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

        in_thinking = False
        in_text = False
        async for event, _metadata in agent.astream(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
            stream_mode="messages",
        ):
            # print(event)
            # continue
            if not isinstance(event, AIMessageChunk) or not event.content:
                continue
            for block in event.content:
                if not isinstance(block, dict):
                    continue
                if block.get("thinking"):
                    if not in_thinking:
                        print("Thinking: ", end="", flush=True)
                        in_thinking = True
                    print(block.get("thinking", ""), end="", flush=True)
                else:
                    if in_thinking:
                        print()
                        in_thinking = False
                    if not in_text:
                        print("Agent: ", end="", flush=True)
                        in_text = True
                    print(block.get("text", ""), end="", flush=True)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
