import os
import json
from dotenv import load_dotenv
import streamlit as st
from pydantic import BaseModel, Field
from typing import List, Literal, Optional

# Import ChatGroq for the free, fast Llama 3 model
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

# --- 1. Define Strict Pydantic Schema ---
class ActionItem(BaseModel):
    task: str = Field(description="A concise, actionable task title")
    assignee: str = Field(description="The person responsible (e.g., 'John', 'Unassigned')")
    priority: Literal["High", "Medium", "Low"] = Field(description="Task priority level")
    due_date: str = Field(description="Expected due date (e.g., 'Next Friday', '2024-11-01', or 'TBD')")
    description: str = Field(description="Detailed context or sub-tasks for this item")

class MeetingOutput(BaseModel):
    meeting_summary: str = Field(description="A brief 2-3 sentence summary of the meeting")
    action_items: List[ActionItem] = Field(description="List of actionable tasks extracted from the transcript")

# --- 2. Initialize LangChain with Groq ---
@st.cache_resource
def get_llm():
    # Using Llama 3 via Groq (Free, incredibly fast)
    llm = ChatGroq(
        model="llama-3.1-8b-instant", 
        temperature=0.1
    )
    return llm

# --- 3. Streamlit UI ---
st.set_page_config(page_title="AI Jira Generator", page_icon="🎫", layout="wide")

st.title("🎫 Meeting Transcript to Jira Tickets")
st.markdown("Paste your messy meeting notes below. The AI will extract a summary and generate structured, ready-to-use Jira tickets.")

# Sample data for easy testing
SAMPLE_TRANSCRIPT = """
Hey team, thanks for joining. So, for the Q3 launch, Sarah, I need you to update the landing page copy by next Friday. 
Make sure it highlights the new dark mode feature. 
Mike, can you look into the API timeout issues we've been seeing? That's a high priority, let's get it fixed by Wednesday. 
Also, we need to schedule a design review for the mobile app, let's say sometime next month. 
Oh, and someone needs to update the README on the GitHub repo to reflect the new Python 3.11 requirements.
"""

with st.expander("📝 Click here to load a sample transcript"):
    st.text(SAMPLE_TRANSCRIPT)

# User Input
transcript = st.text_area("Paste Meeting Transcript:", height=250, value=SAMPLE_TRANSCRIPT)

if st.button("🪄 Generate Jira Tickets", type="primary"):
    if not transcript.strip():
        st.warning("Please paste a transcript first.")
    else:
        with st.spinner("🧠 AI is analyzing transcript and structuring data..."):
            try:
                llm = get_llm()
                
                # Create a prompt that explicitly asks for JSON
                prompt = f"""Extract the meeting summary and action items from this transcript. 
Return the response in valid JSON format matching this schema:
{{
    "meeting_summary": "string",
    "action_items": [
        {{
            "task": "string",
            "assignee": "string",
            "priority": "High/Medium/Low",
            "due_date": "string",
            "description": "string"
        }}
    ]
}}

Transcript:
{transcript}

JSON Response:"""
                
                # Get response from LLM
                response = llm.invoke(prompt)
                response_content = response.content.strip()
                
                # Parse the JSON response
                try:
                    # Try to parse as JSON directly
                    result_dict = json.loads(response_content)
                except json.JSONDecodeError:
                    # If it fails, try to extract JSON from markdown code blocks
                    if "```json" in response_content:
                        json_str = response_content.split("```json")[1].split("```")[0].strip()
                        result_dict = json.loads(json_str)
                    elif "```" in response_content:
                        json_str = response_content.split("```")[1].split("```")[0].strip()
                        result_dict = json.loads(json_str)
                    else:
                        raise ValueError("Could not parse JSON from response")
                
                # Convert to Pydantic model for validation
                result = MeetingOutput(**result_dict)
                
                # Display Summary
                st.success("✅ Processing Complete!")
                st.subheader("📋 Meeting Summary")
                st.info(result.meeting_summary)
                
                # Display Action Items as "Tickets"
                st.subheader("🎫 Generated Jira Tickets")
                
                for i, item in enumerate(result.action_items, 1):
                    with st.container(border=True):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"### 📌 {item.task}")
                            st.markdown(f"**Description:** {item.description}")
                            st.markdown(f"**Assignee:** 👤 {item.assignee} | **Due:** 📅 {item.due_date}")
                        with col2:
                            # Color-code priority
                            if item.priority == "High":
                                st.markdown("🔴 **High Priority**")
                            elif item.priority == "Medium":
                                st.markdown("🟡 **Medium Priority**")
                            else:
                                st.markdown("🟢 **Low Priority**")
                        
                        # Mock "Send to Jira" button
                        if st.button(f"📤 Send Ticket {i} to Jira", key=f"btn_{i}"):
                            st.toast(f"Ticket '{item.task}' successfully pushed to Jira API!", icon="✅")
                            
                # Show the raw JSON (Recruiters love seeing the structured data)
                with st.expander("🔧 View Raw JSON Payload (For API Integration)"):
                    st.json(result.model_dump())
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.info("Tip: Make sure your GROQ_API_KEY is correctly set in the .env file.")