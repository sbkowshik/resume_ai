import os
from typing import Dict, List
import gradio as gr
import fitz  # PyMuPDF
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from agents.base_agent import create_agent, create_initial_state

# Load environment variables
load_dotenv()

def extract_text_from_pdf(file_obj) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        file_obj: File object containing the PDF
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        doc = fitz.open(stream=file_obj.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        raise gr.Error(f"Error processing PDF: {str(e)}")

class ChatState:
    """
    Class to maintain chat state and history.
    """
    def __init__(self):
        self.resume_content: str = ""
        self.company: str = ""
        self.role: str = ""
        self.job_description: str = ""
        self.chat_history: List[Dict] = []
        self.agent = create_agent()

chat_state = ChatState()

def process_resume(file_obj) -> str:
    """Process uploaded resume and update state."""
    if file_obj is None:
        raise gr.Error("Please upload a resume first!")
    
    text = extract_text_from_pdf(file_obj)
    chat_state.resume_content = text
    return "Resume processed successfully!"

def update_job_details(company: str, role: str, description: str) -> str:
    """Update job-related details in the state."""
    chat_state.company = company
    chat_state.role = role
    chat_state.job_description = description
    return "Job details updated successfully!"

def chat(message: str, history: List[Dict]) -> tuple:
    """
    Process chat messages and maintain conversation history.
    
    Args:
        message: User's input message
        history: Chat history
        
    Returns:
        tuple: Updated response and history
    """
    # Validate required inputs
    if not chat_state.resume_content:
        raise gr.Error("Please upload your resume first!")
    if not all([chat_state.company, chat_state.role, chat_state.job_description]):
        raise gr.Error("Please fill in all job details first!")
    
    # Create initial state for the agent
    initial_state = create_initial_state(
        resume_content=chat_state.resume_content,
        role=chat_state.role,
        company=chat_state.company,
        job_description=chat_state.job_description
    )
    
    # Add existing chat history
    initial_state["messages"] = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in history
    ]
    
    # Run the agent
    result = chat_state.agent.invoke({
        "state": initial_state,
        "input_str": message
    })
    
    # Get the last assistant message
    response = result["messages"][-1]["content"]
    
    # Update chat history
    chat_state.chat_history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": response}
    ]
    
    return response, chat_state.chat_history

# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Resume Analysis and Job Chat Assistant")
    
    with gr.Row():
        # Left side - Inputs
        with gr.Column(scale=1):
            gr.Markdown("### Upload Resume and Job Details")
            
            file_input = gr.File(
                label="Upload Resume (PDF)",
                file_types=[".pdf"]
            )
            resume_status = gr.Textbox(
                label="Resume Status",
                interactive=False
            )
            
            company_input = gr.Textbox(
                label="Company Name",
                placeholder="Enter company name..."
            )
            role_input = gr.Textbox(
                label="Job Title",
                placeholder="Enter job title..."
            )
            job_desc_input = gr.Textbox(
                label="Job Description",
                placeholder="Enter job description...",
                lines=5
            )
            
            update_button = gr.Button("Update Job Details")
            job_status = gr.Textbox(
                label="Job Details Status",
                interactive=False
            )
        
        # Right side - Chat
        with gr.Column(scale=1):
            gr.Markdown("### Chat with AI Assistant")
            chatbot = gr.Chatbot(
                label="Chat History",
                height=400
            )
            msg_input = gr.Textbox(
                label="Your message",
                placeholder="Type your message here...",
                lines=2
            )
            clear_button = gr.Button("Clear Chat")
    
    # Event handlers
    file_input.change(
        fn=process_resume,
        inputs=[file_input],
        outputs=[resume_status]
    )
    
    update_button.click(
        fn=update_job_details,
        inputs=[company_input, role_input, job_desc_input],
        outputs=[job_status]
    )
    
    msg_input.submit(
        fn=chat,
        inputs=[msg_input, chatbot],
        outputs=[msg_input, chatbot]
    )
    
    clear_button.click(
        lambda: ([], None),
        outputs=[chatbot, msg_input]
    )

if __name__ == "__main__":
    demo.launch()