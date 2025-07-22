# 1. Clone and setup
git clone https://github.com/nordeim/Context7-MCP-RAG-Agent
cd Context7-MCP-RAG-Agent
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your OpenAI key

# 3. Run
python -m src.cli
