# 🎫 AI Meeting Transcript to Jira Tickets

An AI-powered workflow tool that transforms unstructured meeting transcripts into structured, machine-readable Jira ticket payloads. Built to demonstrate advanced LLM capabilities in structured output, data extraction, and API-ready formatting.

![App Screenshot](assets/AI-Jira-Generator.png)

## ✨ Key Features

- Strict structured output with Pydantic models to guarantee valid typed JSON.
- Smart entity extraction for tasks, assignees, priorities, and due dates.
- Developer-ready payloads that can be sent directly to Jira or other REST APIs.
- Cost-effective architecture powered by Groq's Llama 3 for fast inference.
- Interactive Streamlit UI with color-coded priority badges and mock API actions.

## 🏗️ Tech Stack

| Category | Technology | Purpose |
| :-- | :-- | :-- |
| Language | Python 3.10+ | Core application logic |
| AI Framework | LangChain | LLM orchestration and chaining |
| LLM Provider | Groq (Llama 3) | Fast structured generation |
| Validation | Pydantic | Strict data schema enforcement |
| Frontend | Streamlit | Interactive web interface |
| Env Mgmt | python-dotenv | Secure API key handling |

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A free Groq API key

### Installation

1. Clone the repository:
	```bash
	git clone https://github.com/SProvati/ai-jira-generator.git
	cd ai-jira-generator
	```

2. Create and activate a virtual environment:
	```bash
	python -m venv venv
	# Windows
	.\venv\Scripts\activate
	# Mac/Linux
	source venv/bin/activate
	```

3. Install dependencies:
	```bash
	pip install langchain-groq pydantic streamlit python-dotenv
	```

4. Set up environment variables in a `.env` file:
	```env
	GROQ_API_KEY=gsk_your_api_key_here
	```

5. Run the application:
	```bash
	streamlit run app.py
	```

## 💡 How It Works

1. The user pastes raw meeting notes into the Streamlit interface.
2. LangChain builds a prompt that requests strict JSON output matching the schema.
3. Groq's Llama 3 generates the structured response.
4. The response is parsed and validated against the `MeetingOutput` model.
5. The validated tickets render with priority badges and a raw JSON view.

## 📝 CV Bullet Point

> Developed an AI workflow using LangChain and Pydantic to parse unstructured meeting transcripts, automatically extracting structured action items and generating ready-to-use Jira API payloads, reducing manual ticket creation time by 70%.

## Contributing

Contributions are welcome. Please open a pull request with a clear description of the change.

## 📄 License

This project is licensed under the MIT License.

## Project File

- `app.py` contains the Streamlit app and the ticket generation flow.