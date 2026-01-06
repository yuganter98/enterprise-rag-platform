from typing import Callable, List, Dict

# Metadata describing the tools for the LLM
AVAILABLE_TOOLS = [
    {
        "name": "generate_report",
        "description": "Generates an Excel report of employees. Can filter by department or designation.",
        "parameters": {
            "type": "object",
            "properties": {
                "department": {"type": "string", "description": "Filter by department name"},
                "designation": {"type": "string", "description": "Filter by job title"}
            }
        }
    },
    {
        "name": "send_email",
        "description": "Sends an email to a specific recipient or 'all'. Requires subject and body.",
        "parameters": {
            "type": "object",
            "properties": {
                "to_email": {"type": "string", "description": "Recipient email address or 'all'"},
                "subject": {"type": "string", "description": "Email subject line"},
                "body": {"type": "string", "description": "Email content body"}
            },
            "required": ["to_email", "subject", "body"]
        }
    }
]

def get_tool_by_name(name: str) -> Callable:
    """
    Returns the callable function for the given tool name.
    """
    if name == "generate_report":
        from app.services.report.excel import generate_employee_report
        return generate_employee_report
    elif name == "send_email":
        from app.services.email.sender import send_email
        return send_email
    else:
        raise ValueError(f"Tool {name} not found.")
