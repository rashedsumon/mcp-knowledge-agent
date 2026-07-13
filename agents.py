from crewai import Agent, Task, Crew, Process
from langchain.tools import tool

# Import the functional business logic backing the MCP Server tools locally for multi-agent use
import mcp_server

@tool("Search Bug Tracker")
def search_bug_tracker_tool(query: str) -> str:
    """Wrapper exposing the MCP bug tracker tool to the agent framework."""
    return mcp_server.search_bug_tracker(query)

@tool("Query Knowledge Base")
def query_kb_tool(keyword: str) -> str:
    """Wrapper exposing the MCP knowledge base tool to the agent framework."""
    return mcp_server.query_kb(keyword)

@tool("Search Slack Logs")
def search_slack_logs_tool(channel: str, query: str) -> str:
    """Wrapper exposing the MCP Slack log history search tool."""
    return mcp_server.search_slack_logs(channel, query)

class ResearchAgentGroup:
    """
    Defines CrewAI prompt-driven specialist agents built to explore internal infrastructure 
    and synthesize technical findings into natural language.
    """
    def __init__(self):
        # Base Agent configuration
        self.researcher = Agent(
            role="Internal Data Retrieval Specialist",
            goal="Locate, verify, and cross-reference records across all company datasets.",
            backstory="An automated indexing expert designed to navigate database layers and pull truth metrics.",
            tools=[search_bug_tracker_tool, query_kb_tool, search_slack_logs_tool],
            verbose=True
        )
        
        self.writer = Agent(
            role="Technical Communications Analyst",
            goal="Synthesize raw telemetry, logs, and database text records into pristine, plain-English answers.",
            backstory="A precise communicator that translates database structures into clean technical documentation.",
            verbose=True
        )

    def run_investigation(self, user_question: str, context_history: str = "") -> str:
        task1 = Task(
            description=f"Query the MCP server tools to discover context relevant to this request: '{user_question}'. History context: {context_history}",
            expected_output="A compilation of matched raw records containing IDs, text contents, and tracking metadata.",
            agent=self.researcher
        )

        task2 = Task(
            description="Process the found raw text records. Synthesize into a plain English response. You MUST strictly cite the source IDs (e.g., [BUG-xxxx], [KB-xxxx]) and provide actionable instructions.",
            expected_output="A structured markdown answer citing exact sources and direct diagnostic takeaways.",
            agent=self.writer
        )

        crew = Crew(
            agents=[self.researcher, self.writer],
            tasks=[task1, task2],
            process=Process.sequential
        )
        return crew.kickoff()