from typing import Annotated, Dict, List, TypedDict
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel

# Define the state schema
class AgentState(TypedDict):
    """State for the agent pipeline."""
    resume_content: str
    role: str
    company: str
    job_description: str
    messages: List[Dict]
    next: str

# Define the chat model
model = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7
)

# Define the system prompt
SYSTEM_PROMPT = """You are an AI assistant helping users analyze their resume against job descriptions.
You have access to:
1. Their resume content
2. The company they're applying to
3. The role they're applying for
4. The job description

Use this information to help them understand their fit for the role and suggest improvements.
Be honest but constructive in your feedback.

Current Context:
Company: {company}
Role: {role}
"""

def create_agent() -> StateGraph:
    """
    Create the LangGraph agent pipeline.
    
    Returns:
        StateGraph: The configured agent pipeline
    """
    # Define the chat prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}")
    ])
    
    # Define the agent function
    def agent_function(state: AgentState, input_str: str) -> AgentState:
        """Process the input and update the state."""
        # Format messages
        messages = prompt.format_messages(
            company=state["company"],
            role=state["role"],
            messages=state["messages"],
            input=input_str
        )
        
        # Get response from the model
        response = model.invoke(messages)
        
        # Update state
        state["messages"].append({"role": "user", "content": input_str})
        state["messages"].append({"role": "assistant", "content": response.content})
        
        # Always end after response
        state["next"] = "end"
        return state
    
    # Create the workflow
    workflow = StateGraph(AgentState)
    
    # Add the agent node
    workflow.add_node("agent", agent_function)
    
    # Add the entry point
    workflow.set_entry_point("agent")
    
    # Add the conditional edges
    workflow.add_edge("agent", END)
    
    return workflow

def create_initial_state(
    resume_content: str,
    role: str,
    company: str,
    job_description: str
) -> AgentState:
    """
    Create the initial state for the agent pipeline.
    
    Args:
        resume_content: Content of the resume
        role: Job role
        company: Company name
        job_description: Job description
        
    Returns:
        AgentState: Initial state for the pipeline
    """
    return {
        "resume_content": resume_content,
        "role": role,
        "company": company,
        "job_description": job_description,
        "messages": [],
        "next": "agent"
    }