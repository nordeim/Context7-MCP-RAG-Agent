<div align="center">

<img src="https://raw.githubusercontent.com/nordeim/Context7-MCP-RAG-Agent/refs/heads/main/main_screen.png" alt="Context7 AI Logo" width="800"/>

# 🌌 Context7 AI: The Definitive Terminal Agent

> **A production-grade, terminal-native AI companion for developers, engineered for accuracy with Pydantic-AI and a robust Retrieval-Augmented Generation pipeline.**

[![Python Version](https://img.shields.io/badge/Python-3.11+-3776ab.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-F9A825.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-007ACC.svg?style=for-the-badge&logo=windows)](https://www.docker.com/)
[![Docker Support](https://img.shields.io/badge/Docker-Ready-2496ED.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

</div>

---

**Context7 AI** is a battle-tested, terminal-first AI agent designed for developers who demand accuracy and reliability. Powered by `pydantic-ai` and integrated with the **Context7 Model Context Protocol (MCP)** server, it excels at providing authoritative, up-to-date documentation and technical answers.

This project is not just a demo; it's a complete architectural blueprint for building stable, maintainable, and user-friendly AI applications. It features a rich terminal user interface (TUI), a sophisticated theme engine, persistent conversation history, and a robust, non-streaming backend for maximum stability.

## 📸 Application Showcase

Here is the Context7 AI agent in action, running the "Cyberpunk" theme and providing a detailed, markdown-formatted answer based on retrieved documentation.

![Context7 AI in Action](https://i.imgur.com/gKqC7O7.png)

---

## 🎯 Core Philosophy: Engineered for Accuracy

In an era of generative AI, accuracy is paramount, especially for software development. The core design of Context7 AI is built around a single principle: **minimizing hallucination and maximizing trustworthiness.**

This is achieved through a specific **Agent-Led Synthesis** RAG (Retrieval-Augmented Generation) pattern:

1.  **Strictly Controlled Retrieval:** When a query is received, the agent's first and only permissible action is to use its `search` tool. This tool connects to a trusted, curated knowledge base via the Context7 MCP server. The agent is explicitly forbidden by its system prompt from answering from its internal, pre-trained knowledge.
2.  **Grounded Synthesis:** The documents retrieved from the knowledge base are then passed to the agent in a second step. In this phase, the agent's role is transformed from a "knower" to a "synthesizer." It is instructed to formulate its final answer **exclusively** from the provided text.

This two-step, prompt-engineered pipeline ensures that every response is directly traceable to an authoritative source, making it a reliable companion for professional developers.

---

## 🗂️ Project Structure and Architecture

The codebase is organized into a clean, modular structure that separates concerns and promotes maintainability.

### 📋 Complete File Hierarchy

```
context7-agent/
├── 📁 data/                        # Runtime data (auto-created)
│   └── history.json                # Persisted conversation history
├── 📁 docker/                      # Production Docker deployment assets
│   ├── Dockerfile                  # Multi-stage Dockerfile for a lean production image
│   └── .env.docker                 # Environment variable template for Docker
├── 📁 src/                          # Core application source code
│   ├── __init__.py                 # Makes 'src' a Python package
│   ├── agent.py                    # The core AI agent logic and RAG pipeline
│   ├── cli.py                      # Main application entrypoint and Rich TUI
│   ├── config.py                   # Pydantic-based configuration management
│   ├── history.py                  # Conversation history persistence
│   └── themes.py                   # Theming engine for the TUI
├── .env.example                    # Environment variable template for local dev
├── .gitignore                      # Standard Git ignore rules
├── pyproject.toml                  # Python project metadata (PEP 621)
└── requirements.txt                # Pinned production dependencies
```

### 🔄 Architecture Flowchart

This diagram illustrates the flow of information from the user, through the application's core components, to the external AI services, and back.

```mermaid
flowchart TD
    subgraph "User Interface Layer"
        A[👤 User] -- 1. Enters Query --> B(src/cli.py);
        I[src/themes.py] -- Styles --> B;
    end

    subgraph "Application Core"
        B -- 2. Calls agent.chat() --> C(src/agent.py);
        D[src/config.py] -- Provides Settings --> C;
        E[src/history.py] -- Provides History --> C;
        C -- 7. Returns Final Response --> B;
    end

    subgraph "AI Engine (Pydantic-AI)"
        C -- "3. run(query, history)" --> F(pydantic-ai Agent);
        F -- "4. LLM Call 1: Plan Tool Use" --> G[☁️ OpenAI API];
        G -- "5. Return Tool Call Plan" --> F;
        F -- "6a. Execute MCP Tool Call" --> H{Context7 MCP Server};
        H -- "Retrieves Docs" --> J[📚 Authoritative KB];
        F -- "6b. LLM Call 2: Synthesize Answer from Docs" --> G;
    end
    
    subgraph "Data Persistence"
        E -- R/W --> K[data/history.json];
    end

    B -- 8. Renders Markdown --> A;

    style A fill:#D6B6F9,stroke:#333
    style B fill:#A4D4AE,stroke:#333
    style C fill:#87C4E1,stroke:#333
    style F fill:#F9E07F,stroke:#333
    style G fill:#F9A1A1,stroke:#333
    style H fill:#A2A2A2,stroke:#333
    style J fill:#B4E9E2,stroke:#333
    style K fill:#F9DDA4,stroke:#333
```

### 📁 File Descriptions

| File Path | Purpose & Key Features |
| :--- | :--- |
| **`src/agent.py`** | **The Core AI Brain.** This module orchestrates the entire RAG pipeline. It uses `pydantic-ai` to interface with the LLM and the Context7 MCP server. Its powerful system prompt enforces the strict "retrieve-then-synthesize" logic. It uses a stable, non-streaming `chat` method for maximum reliability. |
| **`src/cli.py`** | **The Terminal User Interface.** This is the main entry point for the application. It uses the `rich` library to create a beautiful and interactive TUI. It is structured as a class (`Context7CLI`) for clean state management and handles all user input, command parsing (`/theme`, `/history`, etc.), and response rendering. |
| **`src/config.py`** | **Configuration Hub.** A modern, robust configuration manager built with `pydantic-settings`. It loads settings from a `.env` file, provides type-safe access to configuration variables, and handles path management using `pathlib`. |
| **`src/history.py`** | **Conversation Memory.** Manages the persistence of conversations. It supports multiple, distinct conversation threads, saves history asynchronously to a JSON file, and provides correctly formatted message lists to the agent. |
| **`src/themes.py`** | **The Visual Engine.** A sophisticated, object-oriented theming system. It provides multiple themes (Cyberpunk, Ocean, Forest, Sunset) with unique color palettes, ASCII art banners, and factory methods for creating themed `rich` components like tables and status spinners. |
| **`docker/Dockerfile`** | **Production Container.** A multi-stage Dockerfile that creates a small, optimized production image by separating build dependencies from runtime dependencies, ensuring a secure and efficient deployment. |
| **`pyproject.toml`** | **Project Definition.** Defines the project metadata, dependencies, and entry points according to modern Python packaging standards (PEP 621). |
| **`requirements.txt`** | **Reproducible Dependencies.** A list of all production Python dependencies, pinned to specific versions to guarantee stable and reproducible builds. |

---

## ✨ Features & Roadmap

This project is a mature foundation with a clear vision for the future.

### ✅ Current Features

#### Core AI Functionality
- **Stable RAG Pipeline:** Employs the "Agent-Led Synthesis" pattern for high-accuracy, grounded responses.
- **`pydantic-ai` Integration:** Built on a stable and powerful agentic framework.
- **Context7 MCP Tooling:** Seamlessly integrates with the Upstash Context7 MCP server for authoritative document retrieval.
- **Multi-Conversation History:** Persists and manages distinct conversation threads, providing context to the agent.

#### Terminal User Experience (TUI)
- **Rich, Object-Oriented Interface:** A beautiful and responsive TUI built with the `rich` library.
- **Advanced Theming Engine:** Four built-in themes (Cyberpunk, Ocean, Forest, Sunset) with custom colors and ASCII art.
- **CLI Command System:** Supports `/exit`, `/theme`, `/history`, and `/clear` for easy application management.
- **Markdown Rendering:** Beautifully renders the agent's markdown responses, including code blocks with syntax highlighting.
- **Status Indicators:** Provides a clean "thinking..." spinner while the agent processes a request.

#### Production Readiness
- **Full Dockerization:** Comes with a multi-stage `Dockerfile` for building lean, production-ready containers.
- **Modern Configuration:** Uses `pydantic-settings` for robust, type-safe configuration from environment variables.
- **Asynchronous Core:** Built on `anyio` for high-performance, asynchronous operations from top to bottom.
- **Pinned Dependencies:** Guarantees stable, reproducible builds via `requirements.txt`.

### 🚀 Roadmap

#### 📅 Immediate Goals (Next 2-4 Weeks)
- [ ] **Enhance Error Handling:** Implement retry logic with exponential backoff for transient network or API errors.
- [ ] **Implement Conversation Switching:** Add a `/conversation <name>` command to allow users to switch between or create new conversation threads from the CLI.
- [ ] **Refine History View:** Add pagination or a "load more" feature to the `/history` command for users with extensive history.
- [ ] **Develop a Test Suite:** Build out a comprehensive test suite using `pytest` and `pytest-asyncio` to cover the agent, config, and history modules.

#### 🌠 Long-term Vision (3-6 Months)
- [ ] **Introduce Streaming (With a Caching Layer):** Re-investigate a stable streaming implementation, potentially paired with a caching layer. The agent could first return a cached (and therefore instant) response while generating a fresh one in the background, providing the best of both worlds.
- [ ] **Advanced Search Tools:** Extend the agent's capabilities with tools that allow filtering of retrieved documents by date, source, or tags directly from the user's prompt.
- [ ] **Bookmark and Export:** Implement `/bookmark` and `/export` commands to allow users to save important responses and export conversations to Markdown or JSON.
- [ ] **VS Code Extension:** Develop a companion extension to bring the Context7 agent directly into the developer's IDE for seamless workflow integration.

---

## 🚀 Deployment & User Guide

This section provides comprehensive instructions for setting up, deploying, and using the Context7 AI agent.

### 🖥️ Local Development Setup

#### Prerequisites
- **Python 3.11+**
- **Node.js 18+** (Required by the Context7 MCP server, which is run via `npx`)
- An **OpenAI API Key**

#### Quick Start Instructions
1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/nordeim/Context7-MCP-RAG-Agent
    cd Context7-MCP-RAG-Agent
    ```

2.  **Set Up a Virtual Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Your Environment:**
    *   Copy the example environment file:
        ```bash
        cp .env.example .env
        ```
    *   Edit the `.env` file with your favorite text editor and add your OpenAI API key:
        ```ini
        # .env
        OPENAI_API_KEY="sk-..."
        ```

5.  **Run the Application:**
    ```bash
    python -m src.cli
    ```

### 🐳 Production Deployment with Docker

Running the agent in a Docker container is the recommended method for production and isolated environments.

1.  **Build the Docker Image:**
    From the root of the project directory, run:
    ```bash
    docker build -t context7-agent:latest -f docker/Dockerfile .
    ```

2.  **Run the Container:**
    ```bash
    docker run -it \
      --name context7-ai \
      --rm \
      -e OPENAI_API_KEY="sk-your-key-here" \
      -v "$(pwd)/data:/app/data" \
      context7-agent:latest
    ```
    *   `-it`: Runs the container in interactive mode, attaching your terminal.
    *   `--name`: Assigns a convenient name to the container.
    *   `--rm`: Automatically removes the container when it exits.
    *   `-e`: Passes your OpenAI API key as an environment variable.
    *   `-v`: Mounts the local `data` directory into the container, so your `history.json` persists even after the container is removed.

### 🏢 Specialized Deployment: POS Machine or Server

This guide provides instructions for deploying the agent as a background `systemd` service on a modern Linux system (e.g., Ubuntu 20.04+, Debian 11+, CentOS 8+).

1.  **Save the Installation Script:**
    Create a file named `install_context7.sh` on the target machine and paste the following content into it.

    ```bash
    #!/bin/bash
    # install_context7.sh - Automated installer for the Context7 AI Agent
    set -e

    # --- Configuration ---
    APP_USER="context7"
    APP_DIR="/opt/context7-agent"
    GIT_REPO_URL="https://github.com/your-username/context7-agent.git" # IMPORTANT: Change this URL
    OPENAI_API_KEY="sk-your-key-here" # IMPORTANT: Change this key

    echo "🚀 Starting Context7 AI Agent installation..."

    # 1. System Dependencies
    echo "📦 Updating package lists and installing dependencies..."
    sudo apt-get update
    sudo apt-get install -y python3.11 python3.11-venv git curl

    echo "📦 Installing Node.js 18.x..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs

    # 2. Application Setup
    echo "👤 Creating application user '$APP_USER'..."
    sudo useradd -m -d /opt/$APP_USER -s /bin/bash $APP_USER || echo "User $APP_USER already exists."

    echo "⏬ Cloning application into $APP_DIR..."
    sudo git clone "$GIT_REPO_URL" "$APP_DIR"
    sudo chown -R $APP_USER:$APP_USER "$APP_DIR"

    echo "🐍 Setting up Python virtual environment..."
    sudo -u $APP_USER bash -c "cd $APP_DIR && python3.11 -m venv venv"
    sudo -u $APP_USER bash -c "cd $APP_DIR && source venv/bin/activate && pip install -r requirements.txt"

    # 3. Systemd Service for Daemonization
    echo "⚙️ Creating systemd service file..."
    sudo tee /etc/systemd/system/context7.service > /dev/null <<EOF
    [Unit]
    Description=Context7 AI Agent Service
    After=network.target

    [Service]
    Type=simple
    User=$APP_USER
    Group=$APP_USER
    WorkingDirectory=$APP_DIR
    
    # Load environment variables for the service
    Environment="OPENAI_API_KEY=$OPENAI_API_KEY"
    Environment="PYTHONUNBUFFERED=1"

    ExecStart=$APP_DIR/venv/bin/python -m src.cli
    
    # Restart policy
    Restart=on-failure
    RestartSec=10

    [Install]
    WantedBy=multi-user.target
    EOF

    # 4. Enable and Start the Service
    echo "🚀 Enabling and starting the context7 service..."
    sudo systemctl daemon-reload
    sudo systemctl enable context7.service
    sudo systemctl start context7.service

    echo "✅ Installation complete! The Context7 AI Agent is now running in the background."
    echo "   To view logs, run: sudo journalctl -u context7.service -f"
    echo "   To stop the service, run: sudo systemctl stop context7.service"
    ```

2.  **Make the Script Executable and Run It:**
    ```bash
    chmod +x install_context7.sh
    sudo ./install_context7.sh
    ```

### 🗄️ Database Server Setup (for future use)

While the current application uses a JSON file for history, a production system might evolve to use a relational database. Here’s how to set up a PostgreSQL server using Docker.

```bash
# Pull the latest PostgreSQL 15 image
docker pull postgres:15

# Run the container
docker run -d \
  --name context7-postgres \
  --restart always \
  -e POSTGRES_USER=context7_user \
  -e POSTGRES_PASSWORD=a_very_secure_password \
  -e POSTGRES_DB=context7_db \
  -v postgres_data_volume:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15
```
*   This command starts a PostgreSQL server in the background.
*   The data will be persisted in a Docker volume named `postgres_data_volume`.
*   The future application could connect using the URL: `postgresql://context7_user:a_very_secure_password@localhost:5432/context7_db`.

### 🎮 User Guide

#### Basic Interaction
Simply start the application and type your question at the `You:` prompt.

```
$ python -m src.cli
...
You: Explain Python's GIL
Assistant:
The Global Interpreter Lock (GIL) is a mutex...
```

#### Commands
Use slash commands for application management:

| Command | Description | Example |
| :--- | :--- | :--- |
| `/exit` | Exits the application gracefully. | `/exit` |
| `/theme <name>` | Switches the visual theme. | `/theme ocean` |
| `/history` | Displays a summary of recent conversations. | `/history` |
| `/clear` | Clears the message history for the current conversation. | `/clear` |

---

## 🎉 Community and Support

-   **Found a bug? Have a feature request?** Open an issue on our [GitHub Issues Tracker](https://github.com/your-username/context7-agent/issues).
-   **Want to contribute?** We welcome pull requests! Fork the repository and submit your changes.
-   **Join the conversation:** Find us on our [Community Discord (hypothetical)](https://discord.gg/your-invite-code).

**Ready to experience the future of terminal AI?** 🚀
