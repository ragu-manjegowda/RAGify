"""Define Retrieval and Generation model."""

from langchain_core.messages import SystemMessage
from langchain_core.documents import Document
from langchain_core.tools import tool
from langgraph.graph import (
    END,
    MessagesState,
    StateGraph
)
from langgraph.prebuilt import (
    ToolNode,
    tools_condition
)
from typing_extensions import (
    List,
    TypedDict
)

from llms import (
    create_or_get_llm_client,
    vector_store_client
)


class State(TypedDict):
    """Define state for application."""

    question: str
    context: List[Document]
    answer: str


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    vs_client = vector_store_client()
    retrieved_docs = vs_client.similarity_search(query, k=20)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


def query_or_respond(state: MessagesState):
    """Generate tool call for retrieval or respond."""
    llm_with_tools = create_or_get_llm_client().bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])
    # MessagesState appends messages to state instead of overwriting
    return {"messages": [response]}


tools = ToolNode([retrieve])


def generate(state: MessagesState):
    """Generate answer."""
    # Get generated ToolMessages
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    # Format into prompt
    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Try to stick to context as much as possible."
        "\n\n"
        f"{docs_content}"
    )
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    # Run
    response = create_or_get_llm_client().invoke(prompt)
    return {"messages": [response]}


def compile_and_get_graph():
    """Compile graph and return it."""
    graph_builder = StateGraph(MessagesState)

    # Step 1: Generate an AIMessage that may include a tool-call to be sent.
    graph_builder.add_node(query_or_respond)
    # Step 2: Execute the retrieval.
    graph_builder.add_node(tools)
    # Step 3: Generate a response using the retrieved content.
    graph_builder.add_node(generate)

    graph_builder.set_entry_point("query_or_respond")
    graph_builder.add_conditional_edges(
        "query_or_respond",
        tools_condition,
        {END: END, "tools": "tools"},
    )
    graph_builder.add_edge("tools", "generate")
    graph_builder.add_edge("generate", END)

    graph = graph_builder.compile()

    return graph
