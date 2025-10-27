# AI-Powered-Calendar-Assistant-with-PDF-Q-A# 🤖 AI Demo Multifunction (Python v2)

Converted from your n8n workflow: **AI Demo Multifunction**

---

## 🚀 What It Does
Demonstrates an end-to-end automation architecture:
1. Classifies emails with **OpenAI**
2. Sends Slack messages
3. Implements **RAG** with PDFs + Pinecone + GPT
4. Uses a conversational assistant to **book appointments via Calendar API**

---

## 🧱 Files
ai_demo_multifunction.py # Main orchestrator
config.py # Env & mock configuration
requirements.txt # Dependencies
.env.example # API keys template
README.md # Docs

yaml
Copy code

---

## ⚙️ Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
Fill .env with your API keys, or leave empty for mock mode.

▶️ Run
bash
Copy code
python ai_demo_multifunction.py
🧩 APIs
OpenAI API for text classification and chat

Slack Webhook API

Google Calendar API

Pinecone (mocked placeholder)

🕒 Automation
Run periodically via cron or GitHub Actions:

bash
Copy code
0 9 * * * /usr/bin/python /path/to/ai_demo_multifunction.py
