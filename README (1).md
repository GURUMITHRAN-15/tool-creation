# 🤖 AI Project Management Assistant

A simple AI-powered project management assistant built with Python.

This project connects an AI model with a FastAPI backend and a SQLite database.

Instead of manually sending API requests, you can type a normal sentence and let the AI choose the appropriate tool.

Example:

```text
You: Show my projects
```

The AI can use the `get_projects` tool to retrieve the projects from the database.

---

## 🧠 What Is This Project?

This project is a small AI assistant that can manage projects.

It has three main parts:

```text
AI
 ↓
FastAPI
 ↓
SQLite
```

### AI

The AI understands what the user is asking.

This project uses:

- Ollama
- Qwen 2.5 Coder 7B

### FastAPI

FastAPI provides the backend API.

The AI client communicates with FastAPI to perform project operations.

### SQLite

SQLite stores the project data.

Each project contains:

```text
ID
Name
Language
Year
```

---

## 🔄 How Does It Work?

Suppose the user types:

```text
Add a Python project called Movie App for 2026
```

The process is:

```text
User
 ↓
Qwen AI
 ↓
AI chooses add_project
 ↓
Python executes the tool
 ↓
FastAPI
 ↓
SQLite
 ↓
Project is saved
 ↓
Result goes back to AI
 ↓
AI gives the response
```

The AI does not directly modify the database.

Instead, the AI decides which tool should be used, and Python executes that tool.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | Backend REST API |
| SQLite | Project database |
| Pydantic | Request validation |
| Ollama | Runs the AI locally |
| Qwen 2.5 Coder 7B | AI model |
| Requests | Communicates with the API |
| python-dotenv | Loads environment variables |
| Cloudflare Tunnel | Optional temporary public access |

---

## 📁 Project Structure

```text
tool-creation/
│
├── main.py
├── ai_client.py
├── client.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── .env              ← local only
├── projects.db       ← local database
└── venv/             ← local virtual environment
```

The following should stay local and should not be uploaded to GitHub:

- `.env`
- `projects.db`
- `venv/`

---

## 📄 Files Explained

### `main.py`

This is the FastAPI backend.

It creates the API and handles the project database operations.

The API contains:

```text
GET     /projects
POST    /projects
PUT     /projects/{project_id}
PATCH   /projects/{project_id}
DELETE  /projects/{project_id}
```

In simple words:

```text
GET     → Show projects
POST    → Add a project
PUT     → Replace a project
PATCH   → Update part of a project
DELETE  → Delete a project
```

---

### `ai_client.py`

This is the AI side of the project.

It:

- Connects to Ollama
- Sends requests to Qwen
- Defines the tools
- Executes the tools
- Communicates with the FastAPI backend
- Provides the interactive terminal assistant

Current tools:

```text
get_projects
add_project
update_project
delete_project
```

Example:

```text
User:
Show my projects

↓

AI:
I should use get_projects

↓

Python:
Executes get_projects()

↓

FastAPI:
GET /projects

↓

SQLite:
Returns project data
```

---

### `client.py`

This is a simple Python client for communicating with the FastAPI backend.

It demonstrates how a Python program can send requests to the API.

---

### `projects.db`

This is the SQLite database.

It stores project information such as:

```text
ID
Name
Language
Year
```

Example:

```text
ID    Name          Language    Year
1     RAG Bot       Python      2026
2     Banking App   Java        2028
```

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/GURUMITHRAN-15/tool-creation.git
```

Move into the project:

```bash
cd tool-creation
```

---

## 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

You should see:

```text
(venv)
```

at the beginning of your terminal.

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Install Ollama

Install Ollama on your computer.

Then download the Qwen model:

```powershell
ollama pull qwen2.5-coder:7b
```

Check the installed models:

```powershell
ollama list
```

You should see:

```text
qwen2.5-coder:7b
```

---

## 5. Create the `.env` File

Create a file named:

```text
.env
```

Add:

```env
API_KEY=my-secret-key
API_URL=http://127.0.0.1:8000
```

### Why use `.env`?

The `.env` file stores configuration and secret values outside the Python source code.

The `.env` file is also included in `.gitignore`, so it should not be uploaded to GitHub.

---

## 6. Start the FastAPI Backend

Open a terminal inside the project and run:

```powershell
uvicorn main:app --reload
```

The API should start at:

```text
http://127.0.0.1:8000
```

---

## 7. Open FastAPI Documentation

FastAPI automatically creates interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

From there, you can see and test the API endpoints.

---

## 8. Start the AI Assistant

Open another terminal.

Go to the project:

```powershell
cd E:\WORK-SPACE\plugins
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Run:

```powershell
python ai_client.py
```

You should see:

```text
======================================
🤖 Project AI Assistant
======================================
Type 'exit' to quit.
```

Now you can type requests.

---

# 💬 Examples

## Show Projects

```text
You: Show my projects
```

The assistant uses:

```text
get_projects
```

and retrieves the data from the backend.

---

## Add a Project

```text
You: Add a Python project called Movie App for 2026
```

The AI understands:

```text
Name     → Movie App
Language → Python
Year     → 2026
```

Then it uses:

```text
add_project
```

---

## Update a Project

```text
You: Update project 15
```

The AI can use:

```text
update_project
```

with the project ID.

---

## Delete a Project

```text
You: Delete project 15
```

The AI can use:

```text
delete_project
```

to remove the project.

---

# 🔧 What Is a Tool?

This is one of the main concepts of this project.

An AI model can understand language, but it needs a way to perform actions in an external system.

We give the AI functions called **tools**.

For example:

```text
get_projects
```

means:

> Get the projects from the database.

Another tool:

```text
add_project
```

means:

> Add a new project.

The AI chooses the appropriate tool based on the user's request.

---

# 🧩 Current Tools

## `get_projects`

Gets all projects.

Example:

```text
User:
Show my projects

AI:
get_projects()
```

---

## `add_project`

Adds a new project.

```text
add_project(
    name,
    language,
    year
)
```

---

## `update_project`

Updates an existing project using its ID.

```text
update_project(
    project_id,
    name,
    language,
    year
)
```

---

## `delete_project`

Deletes a project using its ID.

```text
delete_project(
    project_id
)
```

---

# 🔑 API Authentication

The FastAPI backend uses an API key.

The key is stored in:

```text
.env
```

Example:

```env
API_KEY=my-secret-key
```

The client sends the key using the:

```text
X-API-Key
```

HTTP header.

The backend checks the key before allowing access.

The basic flow is:

```text
Client
 ↓
X-API-Key
 ↓
FastAPI
 ↓
Check API key
 ↓
Allow / Reject request
```

---

# 🌐 Optional: Cloudflare Tunnel

Normally, the FastAPI server is available only on the local computer:

```text
http://127.0.0.1:8000
```

A Cloudflare Quick Tunnel can temporarily expose the local API through a public URL.

Run:

```powershell
cloudflared tunnel --url http://127.0.0.1:8000
```

Cloudflare will provide a URL similar to:

```text
https://something.trycloudflare.com
```

Then update the API URL in `.env`:

```env
API_URL=https://something.trycloudflare.com
```

This is optional.

The project can also work completely locally without the tunnel.

> Note: Quick Tunnel URLs are temporary and can change.

---

# 🏗️ Project Architecture

```text
                    USER
                      │
                      ▼
              ┌───────────────┐
              │  AI CLIENT    │
              │  ai_client.py │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │     QWEN      │
              │   via Ollama  │
              └───────┬───────┘
                      │
                 Tool Request
                      │
                      ▼
              ┌───────────────┐
              │     TOOL      │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │    FASTAPI    │
              │    main.py    │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │    SQLITE     │
              │  projects.db  │
              └───────────────┘
```

---

# 🧠 Simple Explanation of the Architecture

Think of the project like this:

### User = Person giving the instruction

```text
"Add my Movie App project"
```

### Qwen = Brain

It understands what the user wants.

### Tool = Action

The AI decides:

```text
add_project
```

### Python = Executor

Python runs the selected tool.

### FastAPI = Backend

FastAPI receives the request and performs the database operation.

### SQLite = Storage

SQLite permanently stores the project information.

So the complete idea is:

```text
User
 ↓
AI understands
 ↓
AI chooses a tool
 ↓
Python executes the tool
 ↓
FastAPI handles the request
 ↓
SQLite stores/retrieves the data
 ↓
Result goes back to AI
 ↓
AI responds to the user
```

---

# 🧠 What I Learned

This project helped me understand how an AI application can connect to normal software.

The important flow is:

```text
User
 ↓
LLM
 ↓
Tool Calling
 ↓
Python Function
 ↓
REST API
 ↓
Database
```

The AI understands the user's request.

The Python tools perform the actual actions.

FastAPI provides the backend.

SQLite stores the data.

---

# ✅ Current Features

- [x] FastAPI backend
- [x] SQLite database
- [x] GET API
- [x] POST API
- [x] PUT API
- [x] PATCH API
- [x] DELETE API
- [x] Pydantic validation
- [x] API key authentication
- [x] `.env` configuration
- [x] Python API client
- [x] Ollama integration
- [x] Qwen 2.5 Coder integration
- [x] AI tool calling
- [x] Project management tools
- [x] Interactive terminal assistant
- [x] Cloudflare Tunnel support

---

# 🚧 Future Improvements

Planned improvements:

- [ ] Multi-step agent workflow
- [ ] Find projects by name
- [ ] Update projects using natural language
- [ ] Delete confirmation
- [ ] Better conversation memory
- [ ] Better tool validation
- [ ] Modular project structure
- [ ] Logging
- [ ] Improved security
- [ ] Deployment
- [ ] MCP integration

---

# 👨‍💻 Author

**Gurumithran V**

B.Tech ECE Student

GitHub: [GURUMITHRAN-15](https://github.com/GURUMITHRAN-15)
