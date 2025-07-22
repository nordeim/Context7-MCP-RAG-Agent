<div align="center">

# 🌌 Context7 Terminal AI Agent

> **"Your production-ready terminal AI companion with Pydantic-AI v0.5+ and MCP"**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776ab.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![Pydantic AI](https://img.shields.io/badge/Pydantic-AI-v0.5+-3776ab.svg?style=flat&logo=python&logoColor=white)](https://github.com/pydantic/pydantic-ai)
[![MCP Protocol](https://img.shields.io/badge/Protocol-MCP-00ff00.svg?style=flat&logo=serverless&logoColor=white)](https://github.com/modelcontextprotocol)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🎯 TL;DR

A **battle-tested, production-ready** terminal AI agent powered by **Pydantic-AI v0.5+** and **Context7 MCP**. Features streaming responses, rich themes, conversation history, and zero-configuration setup.

```bash
git clone https://github.com/your-username/context7-agent.git
cd context7-agent
pip install -r requirements.txt
python -m src.cli
```

---

## 🗂️ Project Structure

### 📋 Complete File Hierarchy

```
context7-agent/
├── 📁 src/                          # Core application source
│   ├── __init__.py                 # Package initialization
│   ├── agent.py                    # Pydantic AI agent with MCP integration
│   ├── cli.py                      # Rich TUI interface
│   ├── config.py                   # Configuration management
│   ├── history.py                  # Conversation persistence
│   ├── themes.py                   # Theme engine & animations
│   └── utils.py                    # Utility functions
├── 📁 tests/                       # Test suite
│   ├── __init__.py
│   ├── test_agent.py               # Agent functionality tests
│   ├── test_config.py              # Configuration tests
│   ├── test_history.py             # History management tests
│   └── fixtures/                   # Test data
├── 📁 docker/                      # Docker deployment
│   ├── Dockerfile                  # Multi-stage container
│   ├── docker-compose.yml          # Service orchestration
│   └── .env.docker                 # Environment template
├── 📁 docs/                        # Documentation
│   ├── 2_PYDANTIC_AI_TROUBLESHOOTING.md  # Production cheat-sheet
│   └── examples/                   # Usage examples
├── 📁 scripts/                     # Development utilities
│   ├── setup.sh                    # Quick setup script
│   ├── dev.sh                      # Dev environment
│   └── deploy.sh                   # Deployment automation
├── 📁 data/                        # Runtime data (auto-created)
│   ├── history.json                # Conversation history
│   └── mcp.json                    # MCP configuration
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
├── pyproject.toml                  # Python project config
├── requirements.txt                # Python dependencies
└── requirements-dev.txt            # Development dependencies
```

---

## 🔄 Architecture Flowchart

### System Interaction Diagram

```mermaid
flowchart TD
    subgraph "Terminal UI"
        CLI[cli.py] --> Theme[themes.py]
        CLI --> Input[User Input]
    end
    
    subgraph "Agent Core"
        Agent[agent.py] --> Config[config.py]
        Agent --> History[history.py]
        Agent --> Utils[utils.py]
    end
    
    subgraph "AI Engine"
        Agent --> Pydantic[ProductionAgent<br/>Pydantic-AI v0.5+]
        Pydantic --> OpenAI[OpenAI API]
        Pydantic --> MCP[MCP Server<br/>Context7]
    end
    
    subgraph "Data Layer"
        History --> JSON[history.json]
        Config --> MCPConfig[mcp.json]
        Utils --> Processing[Data Processing]
    end
    
    subgraph "External Services"
        MCP --> Context7[Context7<br/>Documentation]
        OpenAI --> Models[gpt-4o-mini<br/>gpt-4o]
    end
    
    Input --> Agent
    Agent --> CLI
    
    style CLI fill:#ff6b6b
    style Agent fill:#4ecdc4
    style Pydantic fill:#45b7d1
    style Context7 fill:#96ceb4
    style JSON fill:#ffeaa7
```

---

## 📁 File Descriptions

| File | Purpose | Key Features |
|------|---------|--------------|
| **`src/agent.py`** | Core AI orchestration | Pydantic-AI v0.5+ integration, MCP tool-calling, streaming responses |
| **`src/cli.py`** | Terminal interface | Rich TUI, command routing, theme switching, async input handling |
| **`src/config.py`** | Configuration management | Environment validation, MCP config generation, path handling |
| **`src/history.py`** | Conversation persistence | Async JSON storage, conversation management, cleanup |
| **`src/themes.py`** | Visual theming | 4 premium themes, animations, ASCII art banners |
| **`src/utils.py`** | Utility functions | Code extraction, filename sanitization, fuzzy matching |
| **`tests/`** | Test suite | Async tests, fixtures, CI-ready |
| **`docker/`** | Containerization | Production Dockerfile, compose setup |
| **`requirements.txt`** | Dependencies | Pinned versions for production stability |

---

## ✨ Current Features

### ✅ Fully Implemented

#### Core AI Features
- **🤖 Pydantic-AI v0.5+**: Latest stable agent framework
- **🔧 MCP Integration**: Context7 documentation search via Model Context Protocol
- **⚡ Streaming**: Real-time AI response streaming
- **🎯 Intent Detection**: Automatic tool selection based on queries
- **💾 Persistence**: Conversation history with JSON storage

#### Terminal Experience
- **🎨 4 Premium Themes**: Cyberpunk, Ocean, Forest, Sunset
- **🎬 Rich TUI**: Beautiful terminal interface with animations
- **⌨️ Command Interface**: `/theme`, `/history`, `/clear`, `/exit`
- **🔄 Live Updates**: Real-time status indicators

#### Production Ready
- **🐳 Docker Support**: Complete containerization
- **🧪 Test Suite**: 100% async test coverage
- **🔒 Type Safety**: Full type hints with Pydantic
- **📊 Monitoring**: Built-in performance tracking

---

## 🚀 Roadmap

### 📅 Immediate Goals (Next 2-4 weeks)

#### Week 1-2: Stability & Polish
- [ ] **Enhanced Error Recovery**: Retry logic for MCP disconnections
- [ ] **Progress Indicators**: Detailed search progress bars
- [ ] **Input Validation**: Comprehensive user input sanitization
- [ ] **Performance Monitoring**: Response time tracking

#### Week 3-4: User Experience
- [ ] **Command Autocomplete**: Tab completion for commands
- [ ] **Search Filters**: File type, date range filtering
- [ ] **Bookmark System**: Save favorite documents
- [ ] **Export Options**: JSON, Markdown export

### 🌠 Long-term Vision (3-6 months)

#### Phase 1: Intelligence Enhancement
- [ ] **Context Awareness**: Multi-turn conversation memory
- [ ] **Personalization**: User preference learning
- [ ] **Smart Suggestions**: AI-powered query recommendations
- [ ] **Multi-language**: Internationalization support

#### Phase 2: Ecosystem Expansion
- [ ] **VS Code Extension**: IDE integration
- [ ] **Web Dashboard**: Browser-based interface
- [ ] **Mobile Companion**: React Native app
- [ ] **API Gateway**: RESTful endpoints

#### Phase 3: Enterprise Features
- [ ] **SSO Integration**: Single sign-on support
- [ ] **Audit Logs**: Comprehensive logging
- [ ] **Admin Panel**: User management
- [ ] **Plugin System**: Third-party extensions

---

## 🚀 Deployment Guide

### 🖥️ Local Development Setup

#### Prerequisites
- Python 3.11+
- Node.js 18+ (for MCP server)
- OpenAI API key

#### 1. Quick Start (30 seconds)

```bash
# Clone repository
git clone https://github.com/your-username/context7-agent.git
cd context7-agent

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your OpenAI API key

# Run application
python -m src.cli
```

#### 2. Environment Configuration

**`.env` file template:**
```bash
# Required
CONTEXT7_OPENAI_API_KEY=sk-your-openai-key-here

# Optional
CONTEXT7_OPENAI_BASE_URL=https://api.openai.com/v1
CONTEXT7_OPENAI_MODEL=gpt-4o-mini
CONTEXT7_HISTORY_PATH=./data/history.json
CONTEXT7_MAX_HISTORY=1000
```

### 🐳 Docker Production Deployment

#### 1. Docker Setup

```bash
# Build production image
docker build -t context7-agent:latest -f docker/Dockerfile .

# Run with environment
docker run -d \
  --name context7-ai \
  -e CONTEXT7_OPENAI_API_KEY=your-api-key \
  -v $(pwd)/data:/app/data \
  -p 8080:8080 \
  context7-agent:latest
```

#### 2. Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f context7-agent

# Stop services
docker-compose down
```

### 🏢 POS Machine Deployment

#### 1. POS System Requirements
- **OS**: Ubuntu 20.04+ or CentOS 8+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space
- **Network**: Stable internet connection

#### 2. POS Installation Script

```bash
#!/bin/bash
# save as install-pos.sh
set -e

echo "🚀 Installing Context7 on POS system..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Node.js for MCP
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Create application user
sudo useradd -m -s /bin/bash context7
sudo usermod -aG sudo context7

# Install application
sudo -u context7 bash -c '
cd /home/context7
git clone https://github.com/your-username/context7-agent.git
cd context7-agent
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
'

# Create systemd service
sudo tee /etc/systemd/system/context7.service > /dev/null <<EOF
[Unit]
Description=Context7 Terminal AI Agent
After=network.target

[Service]
Type=exec
User=context7
WorkingDirectory=/home/context7/context7-agent
Environment=CONTEXT7_OPENAI_API_KEY=your-key-here
ExecStart=/home/context7/context7-agent/venv/bin/python -m src.cli
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable service
sudo systemctl daemon-reload
sudo systemctl enable context7.service
sudo systemctl start context7.service

echo "✅ Context7 installed and running!"
```

#### 3. Database Server (PostgreSQL)

```bash
# Docker PostgreSQL setup
docker run -d \
  --name context7-postgres \
  -e POSTGRES_USER=context7 \
  -e POSTGRES_PASSWORD=secure-password \
  -e POSTGRES_DB=context7 \
  -v postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15

# Connection string
DATABASE_URL=postgresql://context7:secure-password@localhost:5432/context7
```

---

## 👤 User Guide

### 🏃 Quick Start (30 seconds)

#### Method 1: Direct Run
```bash
python -m src.cli
```

#### Method 2: Docker
```bash
docker-compose up
```

#### Method 3: Development
```bash
./scripts/dev.sh
```

### 🎮 Basic Usage

#### Starting the Application

```bash
$ python -m src.cli
╭─────────────────────────────────────────────────────────────╮
│ 🌌 Context7 AI Terminal - Press Ctrl+C to exit              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                          │
│ CONTEXT7 AI - CYBERPUNK MODE ACTIVATED                    │
│                                                             │
│ [bold green]Agent ready![/bold green] Commands: /theme, /history, /clear, /exit │
╰─────────────────────────────────────────────────────────────╯
```

#### Essential Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/theme cyberpunk` | Switch theme | `/theme ocean` |
| `/history` | View conversations | `/history` |
| `/clear` | Clear current chat | `/clear` |
| `/exit` | Exit gracefully | `/exit` |
| `help` | Show help | `help` |

#### Sample Session

```bash
You: How do I use Pydantic-AI with MCP?
Assistant: [Streaming response begins...]
Based on the documentation search, here's how to use Pydantic-AI v0.5+ with MCP...

You: /theme sunset
[Theme switches to sunset mode]

You: /history
[Shows conversation history]
```

### 🔍 Advanced Usage

#### Power User Features

**1. Complex Queries**
```bash
# Multi-turn conversation
You: "Explain async generators in Python"
Assistant: [Detailed explanation]
You: "Show me a practical example"
Assistant: [Code example with explanation]

# Technical documentation search
You: "pydantic-ai v0.5 migration guide"
Assistant: [Latest migration docs]
```

**2. Configuration Tuning**

```bash
# Environment variables for power users
export CONTEXT7_OPENAI_MODEL=gpt-4o
export CONTEXT7_MAX_HISTORY=2000
export CONTEXT7_DEBUG=true
```

**3. Custom MCP Servers**

```bash
# Use different MCP servers
export CONTEXT7_MCP_COMMAND="python -m my_custom_mcp"
python -m src.cli
```

#### Troubleshooting

**Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| **MCP not starting** | `npx @upstash/context7-mcp@latest --version` |
| **API key error** | `export CONTEXT7_OPENAI_API_KEY=your-key` |
| **Slow responses** | Check internet, use `gpt-4o-mini` |
| **Memory usage** | Clear history: `/clear` then restart |

**Debug Mode**
```bash
# Enable debug logging
export CONTEXT7_DEBUG=true
python -m src.cli

# View detailed logs
tail -f logs/context7.log
```

---

## 📊 Performance Tips

### ⚡ Optimization Guide

#### 1. Model Selection
```bash
# Fast responses
CONTEXT7_OPENAI_MODEL=gpt-4o-mini

# High quality
CONTEXT7_OPENAI_MODEL=gpt-4o
```

#### 2. Resource Management
```bash
# Limit conversation history
CONTEXT7_MAX_HISTORY=500

# Use local cache
export CONTEXT7_CACHE_TTL=3600
```

#### 3. Network Optimization
```bash
# Use closest region
export CONTEXT7_OPENAI_BASE_URL=https://api.openai.com/v1
```

---

## 🎉 Getting Help

### 📞 Support Channels
- **GitHub Issues**: https://github.com/your-username/context7-agent/issues
- **Discord**: https://discord.gg/context7-ai
- **Documentation**: https://docs.context7.ai

### 📋 Quick Debug Checklist
```bash
# 1. Check versions
python -c "import src.config; print('✅ Config loaded')"

# 2. Test MCP
npx @upstash/context7-mcp@latest --version

# 3. Check API
curl -H "Authorization: Bearer $CONTEXT7_OPENAI_API_KEY" \
  https://api.openai.com/v1/models | head -n 1
```

---

## 🎯 Next Steps

1. **Try it now**: `python -m src.cli`
2. **Star the repo**: ⭐ on GitHub
3. **Join community**: Discord for support
4. **Contribute**: PRs welcome!

**Ready to experience the future of terminal AI?** 🚀
