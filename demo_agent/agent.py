from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import ALL_TOOLS


def build_agent():
    model = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        include_thoughts=True,
    )
    model_with_tools = model.bind_tools(ALL_TOOLS)

    async def call_llm(state: MessagesState):
        return {"messages": [await model_with_tools.ainvoke(state["messages"])]}

    def should_continue(state: MessagesState):
        last = state["messages"][-1]
        if hasattr(last, "tool_calls") and last.tool_calls:
            return "tools"
        return END

    tool_node = ToolNode(ALL_TOOLS)

    graph = StateGraph(MessagesState)
    graph.add_node("llm", call_llm)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "llm")
    graph.add_conditional_edges("llm", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "llm")

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)
