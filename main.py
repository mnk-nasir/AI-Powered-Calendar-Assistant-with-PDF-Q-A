#!/usr/bin/env python3
"""
AI Demo Multifunction (Python v2)
---------------------------------
A unified Python version of the n8n AI Demo Multifunction workflow.
It demonstrates:
  • Email classification via OpenAI
  • Slack automation webhook
  • PDF RAG search using Pinecone + GPT
  • Appointment booking via Anthropic-like assistant and Google Calendar API

Runs in mock mode automatically if no API keys are set.
"""

import os
import logging
import requests
from datetime import datetime, timedelta
from openai import OpenAI
from config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("ai_demo_multifunction")
cfg = Config.load_from_env()

# ---------- MOCK HELPERS ----------
def mock_response(name: str):
    log.info(f"[MOCK] Simulating {name}")
    return {"status": "mocked", "action": name}

# ---------- 1. EMAIL CLASSIFICATION ----------
def classify_email(subject: str, body: str):
    """Use OpenAI to classify an email by topic."""
    if cfg.mock:
        return {"category": "automation" if "workflow" in subject.lower() else "music"}

    client = OpenAI(api_key=cfg.OPENAI_API_KEY)
    prompt = f"""Classify this email into one of: Automation, Music.
Subject: {subject}
Body: {body}
Answer with only the category."""
    res = client.chat.completions.create(model="gpt-4o-mini",
                                         messages=[{"role": "user", "content": prompt}])
    return {"category": res.choices[0].message.content.strip().lower()}

def label_email(category: str):
    """Assign label in Gmail API (mocked)."""
    if cfg.mock:
        return mock_response(f"add_label_{category}")
    # Real Gmail API call placeholder
    raise NotImplementedError("Gmail labeling requires OAuth tokens.")

# ---------- 2. SLACK WEBHOOK ----------
def send_slack_message(email: str):
    if not cfg.SLACK_WEBHOOK_URL:
        log.info("[SKIP] Slack webhook not set.")
        return
    data = {"text": f"Data from webhook: {email}"}
    if cfg.mock:
        log.info(f"[MOCK] Slack message: {data}")
        return
    requests.post(cfg.SLACK_WEBHOOK_URL, json=data)
    log.info("Sent Slack message.")

# ---------- 3. RAG PIPELINE ----------
def download_pdf(url: str, filename: str = "whitepaper.pdf"):
    if cfg.mock:
        log.info(f"[MOCK] Downloading PDF {url}")
        return filename
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)
    return filename

def embed_pdf_to_pinecone(pdf_path: str):
    if cfg.mock:
        return mock_response("embed_pdf_to_pinecone")
    raise NotImplementedError("Real Pinecone integration not implemented yet.")

def query_pdf(question: str):
    if cfg.mock:
        return f"[MOCK] Answer for: {question}"
    client = OpenAI(api_key=cfg.OPENAI_API_KEY)
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a PDF RAG assistant."},
                  {"role": "user", "content": question}]
    )
    return res.choices[0].message.content

# ---------- 4. CALENDAR ASSISTANT ----------
def check_availability(start, end):
    if cfg.mock:
        return {"status": "free"}
    url = "https://www.googleapis.com/calendar/v3/freeBusy"
    headers = {"Authorization": f"Bearer {cfg.GOOGLE_API_TOKEN}"}
    payload = {
        "timeMin": start,
        "timeMax": end,
        "timeZone": "Europe/Berlin",
        "items": [{"id": cfg.CALENDAR_EMAIL}],
    }
    res = requests.post(url, headers=headers, json=payload)
    return res.json()

def book_appointment(user_name, user_email, start_time):
    end_time = (datetime.fromisoformat(start_time) + timedelta(minutes=30)).isoformat()
    if cfg.mock:
        return mock_response(f"book_appointment_{user_name}")
    url = f"https://www.googleapis.com/calendar/v3/calendars/{cfg.CALENDAR_EMAIL}/events"
    headers = {"Authorization": f"Bearer {cfg.GOOGLE_API_TOKEN}",
               "Content-Type": "application/json"}
    body = {
        "summary": f"Appointment with {user_name}",
        "start": {"dateTime": start_time, "timeZone": "Europe/Berlin"},
        "end": {"dateTime": end_time, "timeZone": "Europe/Berlin"},
        "attendees": [{"email": cfg.CALENDAR_EMAIL}, {"email": user_email}],
    }
    res = requests.post(url, headers=headers, json=body)
    return res.json()

def run_calendar_assistant(prompt: str):
