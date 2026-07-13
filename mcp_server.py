from fastmcp import FastMCP
from data_loader import KnowledgeDataLoader

# Initialize the production-ready Model Context Protocol Server
mcp = FastMCP("Internal Dataset Server")
data_store = KnowledgeDataLoader().prepare_mock_internal_data()

@mcp.tool()
def search_bug_tracker(query: str) -> str:
    """Search the internal bug tracking system (Jira) for match queries."""
    results = [d for d in data_store if query.lower() in d['content'].lower() or query.lower() in d['id'].lower()]
    if not results:
        return "No matching bugs found in the tracking system."
    return "\n---\n".join([f"[{r['id']}] {r['title']}: {r['content']} Status: {r['status']}" for r in results])

@mcp.tool()
def query_kb(keyword: str) -> str:
    """Query the Knowledge Base (KB) documents using specific system keywords."""
    results = [d for d in data_store if keyword.lower() in d['content'].lower() or keyword.lower() in d['id'].lower()]
    if not results:
        return "No knowledge base documents found matching that criteria."
    return "\n---\n".join([f"[{r['id']}] {r['title']}: {r['content']}" for r in results])

@mcp.tool()
def search_slack_logs(channel: str, query: str) -> str:
    """Search communications history logs within specific Slack channels."""
    # Simulating a dynamic lookup for the iterative query context
    if channel == "cs-alerts" and "BUG-8842" in query:
        return "System Log: No public matches found in #cs-alerts for 'BUG-8842'."
    return f"Logs checked for channel #{channel}. Zero results returned."

if __name__ == "__main__":
    # Start the MCP server process
    mcp.run()