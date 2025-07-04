from mcp.server.fastmcp import FastMCP
# import requests
import jirautil
# Create an MCP server
mcp = FastMCP("Releng jira Server")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def create_releng_promotion_ticket(product: str, build: str, target_registry: str) -> str:
    """
    Create a releng promotion ticket in Jira
    :param product: The product name (accepts only "CDSW" / MODEL-REGISTRY / CML-SERVING) -  MUST be provided by user, do not assume
    :param build: The build identifier (e.g., "2.0.53-b125") -  MUST be provided by user, do not assume
    :param target_registry: The target registry (accepts only "Stage" or "Prod") -  MUST be provided by user, do not assume
    """
    jira = jirautil.ClouderaJira()
    issue = jira.create_releng_promotion_ticket(product, build, target_registry)
    return f"Promotion ticket created: {issue}"

@mcp.tool()
def search_jira_issues(search_string: str, project_key: str = None, max_results: int = 50) -> list:
    """
    Search Jira issues by summary string.

    :param search_string: The string to search in issue summaries
    :param project_key: Limit search to a specific project (optional)
    :param max_results: Max number of issues to return
    :return: List of matching issues (as dicts)
    """
    jira = jirautil.ClouderaJira()
    issues = jira.search_jira_issues(search_string, project_key, max_results)
    return issues

@mcp.tool()
def search_jira_by_assignee(assignee: str, project_key: str = None, max_results: int = 50) -> list:
    """
    Search Jira issues by assignee.

    :param assignee: The assignee's username - this must end with "@cloudera.com" or be a valid account ID
    :param project_key: Limit search to a specific project (optional)
    :param max_results: Max number of issues to return
    :return: List of matching issues (as dicts)
    """
    jira = jirautil.ClouderaJira()
    issues = jira.search_jira_issues_by_assignee(assignee_username=assignee, project_key=project_key, max_results=max_results)
    return issues


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"
