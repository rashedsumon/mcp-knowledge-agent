import mcp_server
from transformers import pipeline

class ResearchAgentGroup:
    """
    Lightweight orchestration group that completely cuts out CrewAI/ChromaDB
    to ensure 100% compatibility across Python 3.14 runtimes.
    """
    def __init__(self):
        # Fallback pipeline using the fine-tuned or base Hugging Face model
        self.generator = pipeline("text-generation", model="gpt2")

    def run_investigation(self, user_question: str, context_history: str = "") -> str:
        # Step 1: Simulated Specialist Extraction Loop (Calling MCP Tools directly)
        search_results = ""
        if "bug" in user_question.lower() or "504" in user_question.lower():
            search_results += mcp_server.search_bug_tracker("database sync 4.2 timeout") + "\n"
            search_results += mcp_server.query_kb("504 error") + "\n"
        
        if "assigned" in user_question.lower() or "notified" in user_question.lower():
            search_results += mcp_server.search_slack_logs("cs-alerts", "BUG-8842") + "\n"

        if not search_results:
            search_results = "No specific internal records matched."

        # Step 2: Synthesis Construction
        prompt = (
            f"Context from internal database:\n{search_results}\n"
            f"Conversation History:\n{context_history}\n"
            f"User Question: {user_question}\n"
            f"Provide a plain English answer citing data source IDs (e.g. [BUG-xxxx]):"
        )
        
        # Safe constraint generation fallback
        res = self.generator(prompt, max_new_tokens=150, num_return_sequences=1)
        return res[0]['generated_text'][len(prompt):].strip()