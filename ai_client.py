from ollama import chat
import requests
import os
import json
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = os.getenv(
    "API_URL",
    "https://agricultural-convertible-statutes-compare.trycloudflare.com"
)

API_KEY = os.getenv("API_KEY")


if not API_KEY:
    raise RuntimeError(
        "API_KEY is missing. Check your .env file."
    )


HEADERS = {
    "X-API-Key": API_KEY
}


MODEL = "qwen2.5-coder:7b"


# ============================================================
# API FUNCTIONS
# ============================================================

def get_projects():
    """
    Get all projects from the FastAPI backend.
    """

    response = requests.get(
        f"{API_URL}/projects",
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


def add_project(name, language, year):
    """
    Add a new project.
    """

    response = requests.post(
        f"{API_URL}/projects",
        headers=HEADERS,
        json={
            "name": name,
            "language": language,
            "year": year
        },
        timeout=15
    )

    response.raise_for_status()

    return response.json()


def update_project(project_id, name, language, year):
    """
    Replace an existing project.
    """

    response = requests.put(
        f"{API_URL}/projects/{project_id}",
        headers=HEADERS,
        json={
            "name": name,
            "language": language,
            "year": year
        },
        timeout=15
    )

    response.raise_for_status()

    return response.json()


def delete_project(project_id):
    """
    Delete an existing project.
    """

    response = requests.delete(
        f"{API_URL}/projects/{project_id}",
        headers=HEADERS,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# AI TOOL DEFINITIONS
# ============================================================

TOOLS = [

    {
        "type": "function",
        "function": {
            "name": "get_projects",
            "description": (
                "Get all projects belonging to the user. "
                "Use this when the user asks to show, list, "
                "view, check, or find their projects."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "add_project",
            "description": (
                "Add a new project to the user's project database."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Project name"
                    },
                    "language": {
                        "type": "string",
                        "description": "Programming language"
                    },
                    "year": {
                        "type": "integer",
                        "description": "Project year"
                    }
                },
                "required": [
                    "name",
                    "language",
                    "year"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "update_project",
            "description": (
                "Update an existing project using its numeric project ID."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "Numeric project ID"
                    },
                    "name": {
                        "type": "string",
                        "description": "New project name"
                    },
                    "language": {
                        "type": "string",
                        "description": "New programming language"
                    },
                    "year": {
                        "type": "integer",
                        "description": "New project year"
                    }
                },
                "required": [
                    "project_id",
                    "name",
                    "language",
                    "year"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "delete_project",
            "description": (
                "Delete a project using its numeric project ID. "
                "Only use this when the user explicitly asks to delete."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "project_id": {
                        "type": "integer",
                        "description": "Numeric project ID"
                    }
                },
                "required": [
                    "project_id"
                ]
            }
        }
    }
]


# ============================================================
# SYSTEM PROMPT
# ============================================================

SYSTEM_PROMPT = """
You are a project management AI assistant.

You are connected to a user's project database.

IMPORTANT RULES:

1. Normal conversation does not require tools.

2. Do NOT call get_projects for greetings or general questions.

3. Use get_projects when the user asks about their projects.

4. Use add_project when the user wants to create or add a project.

5. Use update_project when the user wants to change an existing project.

6. Use delete_project only when the user explicitly wants to delete
   an existing project.

7. Never invent project IDs.

8. If the user gives a project ID, use that ID.

9. If the user refers to a project by name but does not give an ID,
   first use get_projects to find the correct project ID.

10. Never repeatedly call the same tool for the same request.

11. After receiving a tool result, use the result to answer the user.

12. Keep answers concise and clear.
"""


# ============================================================
# TOOL EXECUTION
# ============================================================

def execute_tool(tool_name, arguments):
    """
    Execute the requested backend tool.
    """

    try:

        if tool_name == "get_projects":

            return get_projects()


        if tool_name == "add_project":

            return add_project(
                arguments["name"],
                arguments["language"],
                arguments["year"]
            )


        if tool_name == "update_project":

            return update_project(
                arguments["project_id"],
                arguments["name"],
                arguments["language"],
                arguments["year"]
            )


        if tool_name == "delete_project":

            return delete_project(
                arguments["project_id"]
            )


        return {
            "error": f"Unknown tool: {tool_name}"
        }


    except requests.HTTPError as error:

        return {
            "error": f"API error: {error}"
        }


    except requests.RequestException as error:

        return {
            "error": f"Network error: {error}"
        }


    except Exception as error:

        return {
            "error": str(error)
        }


# ============================================================
# DETECT TOOL REQUEST
# ============================================================

def detect_tool_request(response):
    """
    Detect both:
    
    1. Ollama structured tool calls
    2. Qwen JSON returned inside message.content
    """

    # --------------------------------------------------------
    # STRUCTURED TOOL CALL
    # --------------------------------------------------------

    tool_calls = response.message.tool_calls

    if tool_calls:

        tool_call = tool_calls[0]

        tool_name = tool_call.function.name

        arguments = tool_call.function.arguments

        if isinstance(arguments, str):

            try:
                arguments = json.loads(arguments)

            except json.JSONDecodeError:

                arguments = {}


        return tool_name, arguments


    # --------------------------------------------------------
    # JSON INSIDE MESSAGE CONTENT
    # --------------------------------------------------------

    content = response.message.content

    if not content:

        return None


    try:

        data = json.loads(content)

    except (json.JSONDecodeError, TypeError):

        return None


    if not isinstance(data, dict):

        return None


    if "name" not in data:

        return None


    tool_name = data["name"]

    arguments = data.get(
        "arguments",
        {}
    )


    if not isinstance(arguments, dict):

        arguments = {}


    return tool_name, arguments


# ============================================================
# DIRECT PROJECT LIST REQUEST DETECTION
# ============================================================

def is_project_list_request(text):
    """
    Detect common project-list requests.

    This prevents the small local model from randomly deciding
    whether it should call get_projects.
    """

    text = text.lower().strip()


    patterns = [

        "show my projects",
        "show projects",
        "list my projects",
        "list projects",
        "view my projects",
        "view projects",
        "see my projects",
        "see projects",
        "display my projects",
        "display projects",
        "what are my projects",
        "what projects do i have",
        "what projects have i",
        "my projects",
        "all my projects"

    ]


    return any(
        pattern in text
        for pattern in patterns
    )


# ============================================================
# DIRECT PROJECT LIST HANDLER
# ============================================================

def handle_project_list(user_request):
    """
    Directly get projects and let Qwen format the result.
    """

    print()
    print("🔧 Tool: get_projects")
    print("📦 Arguments: {}")

    print()
    print("⚙️ Executing tool...")


    result = execute_tool(
        "get_projects",
        {}
    )


    print("📡 Tool result:", result)


    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": user_request
        },

        {
            "role": "user",
            "content": (
                "The get_projects tool has already been executed.\n\n"
                f"Database result:\n{json.dumps(result)}\n\n"
                "Answer the original user request using only this result. "
                "Do not call any tools."
            )
        }

    ]


    print()
    print("Thinking...")


    response = chat(
        model=MODEL,
        messages=messages
    )


    return response.message.content


# ============================================================
# NORMAL AI REQUEST
# ============================================================

def ask_ai(user_request):
    """
    Process one user request.
    """

    # --------------------------------------------------------
    # DIRECT PROJECT LIST
    # --------------------------------------------------------

    if is_project_list_request(user_request):

        return handle_project_list(
            user_request
        )


    # --------------------------------------------------------
    # NORMAL AI REQUEST
    # --------------------------------------------------------

    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": user_request
        }

    ]


    print()
    print("Thinking...")


    response = chat(
        model=MODEL,
        messages=messages,
        tools=TOOLS
    )


    # --------------------------------------------------------
    # CHECK TOOL REQUEST
    # --------------------------------------------------------

    tool_request = detect_tool_request(
        response
    )


    # --------------------------------------------------------
    # NORMAL RESPONSE
    # --------------------------------------------------------

    if tool_request is None:

        return response.message.content


    # --------------------------------------------------------
    # TOOL REQUEST
    # --------------------------------------------------------

    tool_name, arguments = tool_request


    print()
    print("🔧 Tool:", tool_name)

    print("📦 Arguments:", arguments)


    # --------------------------------------------------------
    # EXECUTE TOOL
    # --------------------------------------------------------

    print()
    print("⚙️ Executing tool...")


    result = execute_tool(
        tool_name,
        arguments
    )


    print("📡 Tool result:", result)


    # --------------------------------------------------------
    # FINAL AI RESPONSE
    # --------------------------------------------------------

    final_messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": user_request
        },

        {
            "role": "user",
            "content": (
                f"The tool '{tool_name}' was executed.\n\n"
                f"Tool result:\n{json.dumps(result)}\n\n"
                "Now answer the original request using this result. "
                "Do not call any tools."
            )
        }

    ]


    print()
    print("Thinking...")


    final_response = chat(
        model=MODEL,
        messages=final_messages
    )


    return final_response.message.content


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("======================================")
    print("🤖 Project AI Assistant")
    print("======================================")
    print("Type 'exit' to quit.")
    print()


    while True:

        try:

            user_input = input("You: ").strip()


        except (KeyboardInterrupt, EOFError):

            print("\n")
            print("AI: Goodbye! 👋")

            break


        # ----------------------------------------------------
        # EMPTY INPUT
        # ----------------------------------------------------

        if not user_input:

            continue


        # ----------------------------------------------------
        # EXIT
        # ----------------------------------------------------

        if user_input.lower() in [
            "exit",
            "quit",
            "bye"
        ]:

            print()
            print("AI: Goodbye! 👋")

            break


        # ----------------------------------------------------
        # PROCESS REQUEST
        # ----------------------------------------------------

        try:

            answer = ask_ai(
                user_input
            )


            print()
            print("AI:", answer)
            print()


        except Exception as error:

            print()
            print("❌ Error:", error)
            print()


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":

    main()