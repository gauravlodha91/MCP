# Movie MCP Server: VSCode Configuration & Usage Guide

This guide helps you configure and run your Movie MCP (Movie Control Protocol) Server on your local machine using VSCode, and connect to it with the configuration you provided.

---

## Prerequisites

- **Python 3.8+** installed.
- **VSCode** installed ([Download](https://code.visualstudio.com/)).
- **FastAPI** and **Uvicorn** packages installed:
  ```bash
  pip install fastapi uvicorn pydantic sqlite3
  ```
- *(Optional)*: Install the **REST Client** extension in VSCode for easy API testing.

---

## 1. Clone or Prepare Your Movie MCP Server Code

> **Option 1: Clone from GitHub**
>
> - If your code is on GitHub, open VSCode and use the built-in Source Control panel or:
>   ```bash
>   git clone https://github.com/gauravlodha91/MCP.git
>   cd YOUR-REPO
>   code .
>   ```
>
> **Option 2: Create a New Project**
>
> - Open a new folder in VSCode, create a file named `main.py`, and paste your Movie MCP server code into it.

---

## 2. Install Python Dependencies

Open the VSCode terminal and run:

```bash
pip install fastapi uvicorn pydantic
```

---

## 3. Run the MCP Server

In the VSCode terminal, start the server:

```bash
python main.py
```

If you use `uvicorn` directly (sometimes preferred for FastAPI):

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

You should see output like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [XXXX] using StatReload
```

---

## 4. Verify the Server

Open your browser and navigate to:

- [http://127.0.0.1:8000](http://127.0.0.1:8000) — Should show a JSON welcome message.
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) — Interactive Swagger API docs.

---

## 5. Configure the MCP Server in VSCode

If you're using an extension or tool that consumes the `mcp` config (e.g., API Client, custom tool), create a configuration file, e.g. `mcp.json`:

```json
{
  "servers": {
    "movie-mcp-server": {
      "type": "sse",
      "url": "http://127.0.0.1:8000"
    }
  }
}
```

- Place this `mcp.json` in your project root or wherever your tool expects.

---

## 6. Use GitHub Copilot Chat in VSCode

1. **Open GitHub Copilot Chat**:  
   - Click the Copilot icon in the VSCode sidebar, or press <kbd>Ctrl</kbd>+<kbd>I</kbd> (Windows) to open the Copilot Chat panel.

2. **Select the Agent**:  
   - In the chat panel, click the agent selector at the top (usually labeled "Copilot" or "Copilot (Chat)").
   - Choose the agent you want to interact with (e.g., "GitHub Copilot").

3. **Start Asking Your Query**:  
   - Type your question or command in the chat input box and press <kbd>Enter</kbd>.
   - Copilot will respond with code suggestions, explanations, or troubleshooting steps.

4. **Example Screenshots**:

   ![alt text](image.png)

   ![alt text](image-1.png)

   ![alt text](image-2.png)

> **Tip:** You can ask Copilot about your code, request code changes, or get explanations directly in