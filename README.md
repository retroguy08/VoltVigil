# ⚡ AI-Powered Residential Energy Auditor & Load-Shifting Pipeline

An end-to-end, intelligent energy management platform that captures telemetry data from residential distribution networks, conducts engineering-grade load profile analysis using **Google Gemini**, and triggers an automated orchestration pipeline via **n8n** to update Google Sheets logs and deliver real-time actionable directives straight to an engineer's inbox.

---

## 🎯 Architecture Overview
[ User Input / Telemetry Data ]
│
▼
┌──────────────────┐
│  Streamlit App   │  ◄── (Generates Instant AI Load Directives)
└─────────┬────────┘
│
│  (Webhook Payload)
▼
┌──────────────────┐
│   n8n Workflow   │
└─────────┬────────┘
│
┌───────┴───────┐
▼               ▼
┌───────────┐   ┌───────────┐
│  Gemini   │   │  Google   │
│ AI Agent  │   │   Sheets  │
└─────┬─────┘   └─────┬─────┘
│               │
└───────┬───────┘
▼
┌─────────────────┐
│  Gmail Audit    │
│  Notification   │
└─────────────────┘

---

## ✨ Key Features

* **Real-time Telemetry Processing:** Accepts user inputs for household appliance runtimes, peak hour usage, and total daily kilowatt-hour ($\text{kWh}$) consumption.
* **LLM Engineering Analysis:** Integrates Google's `gemini-flash-latest` model to deliver structured load profile breakdowns, cost-impact estimations, and 3-step peak load-shifting directives.
* **Automated Webhook Pipeline:** Leverages an **n8n** automation engine to process data asynchronously without blocking UI execution.
* **Centralized Data Audit:** Automatically logs run telemetry and AI analysis results to a Google Sheets database for long-term power system auditing.
* **Instant Email Dispatch:** Sends formatted engineering reports directly to the user's Gmail inbox upon workflow execution.

---

## 📸 System Screenshots

### 1. Interactive Streamlit Interface & Live AI Analysis
![Streamlit UI & Directives](images/streamlit_app.png)
*The Streamlit web application capturing load parameters and displaying real-time Gemini-generated load-shifting directives.*

### 2. Active n8n Automation Engine
![n8n Workflow Canvas](images/n8n_workflow.png)
*The end-to-end n8n orchestration workflow processing webhook payloads, running Gemini inference, updating Google Sheets, and triggering email delivery.*

### 3. Data Logging & Email Delivery Verification
![Google Sheets & Gmail Proof](images/email_proof.png)
*Successful execution proof: Telemetry logs appended to Google Sheets alongside the delivered audit report inside the inbox.*

---

## 🛠️ Tech Stack & Dependencies

* **Frontend / Dashboard:** [Streamlit](https://streamlit.io/) (Python)
* **AI Model & SDK:** [Google GenAI SDK](https://github.com/google-gemini/deprecations) (`google-genai` / `gemini-flash-latest`)
* **Workflow Automation:** [n8n Cloud](https://n8n.io/)
* **Integrations:** Google Sheets API, Gmail API
* **Deployment:** Streamlit Community Cloud & GitHub Actions

---

## 🚀 Local Setup & Installation

### Prerequisites
* Python 3.10+ installed
* A valid Google AI Studio API Key

### 1. Clone the Repository
bash
[git clone [(https://github.com/retroguy08/VoltVigil).git](https://github.com/retroguy08/VoltVigil.git)
cd YOUR_REPO_NAME](https://github.com/retroguy08/VoltVigil)

2. Install Dependencies
Bash

pip install -r requirements.txt

3. Configure Local Secrets

Create a .streamlit/secrets.toml file in the root directory and add your credentials:
Ini, TOML

GOOGLE_API_KEY = "your_google_ai_studio_api_key_here"
WEBHOOK_URL = "your_n8n_webhook_production_url_here"

4. Run the Streamlit Application
Bash

streamlit run APP.py
