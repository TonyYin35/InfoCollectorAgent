from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI


def build_agent():
    model = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        include_thoughts=True,
    )
    model_with_search = model.bind_tools([{"google_search": {}}])

    async def call_llm(state: MessagesState):
        return {"messages": [await model_with_search.ainvoke(state["messages"])]}

    graph = StateGraph(MessagesState)
    graph.add_node("llm", call_llm)

    graph.add_edge(START, "llm")
    graph.add_edge("llm", END)

    memory = MemorySaver()
    return graph.compile(checkpointer=memory)
