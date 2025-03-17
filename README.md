# Resume AI Assistant

An AI-powered resume analysis tool that helps you evaluate your resume against job descriptions using LangChain and LangGraph.

## Features

- PDF resume upload and parsing
- Job details input (company, role, job description)
- Interactive chat interface with AI assistant
- Smart analysis of resume-job fit
- Constructive feedback and suggestions

## Prerequisites

- Python 3.10 or higher
- OpenAI API key

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/resume_ai.git
cd resume_ai
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:7860)

3. Upload your resume (PDF format)

4. Enter the job details:
   - Company name
   - Job title
   - Job description

5. Use the chat interface to:
   - Ask for resume analysis
   - Get suggestions for improvements
   - Understand your fit for the role
   - Get specific advice about different aspects of your application

## Project Structure

```
resume_ai/
├── app.py              # Main Gradio application
├── agents/
│   └── base_agent.py   # LangGraph agent implementation
├── requirements.txt    # Project dependencies
└── .env               # Environment variables (create this)
```

## Contributing

Feel free to open issues or submit pull requests for improvements.

## License

MIT License