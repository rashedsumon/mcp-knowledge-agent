import streamlit as st
from agents import ResearchAgentGroup
from data_loader import KnowledgeDataLoader

st.set_page_config(page_title="Internal Knowledge AI Agent (MCP)", page_icon="🤖", layout="wide")

# Setup stateful memory tracking for iterative follow-up investigation questions
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "agent_system" not in st.session_state:
    st.session_state.agent_system = ResearchAgentGroup()

st.title("🤖 Internal Dataset Exploration Terminal")
st.caption("Powered by Hugging Face Models, CrewAI Agents, and Model Context Protocol (MCP)")

# Pre-load/Validate local database configuration 
@st.cache_resource
def initialize_system_data():
    loader = KnowledgeDataLoader()
    return loader.prepare_mock_internal_data()

data_context = initialize_system_data()

# Render chat interface layout
st.subheader("Data Investigation Stream")
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

# Process input prompts dynamically matching Scenario 1 & 2
if user_prompt := st.chat_input("Ask a question regarding internal records..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Pull prior conversation states to support true iterative exploration
    history_string = "\n".join([f"{c['role']}: {c['content']}" for c in st.session_state.chat_history[:-1]])

    with st.chat_message("assistant"):
        with st.spinner("Invoking MCP Server & CrewAI orchestration loops..."):
            try:
                # Agent queries the MCP tools and answers 
                response = st.session_state.agent_system.run_investigation(
                    user_question=user_prompt, 
                    context_history=history_string
                )
                # Fallback format checking for the user interface display safety
                response_text = str(response)
                st.markdown(response_text)
                st.session_state.chat_history.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Execution Error encountered: {str(e)}")