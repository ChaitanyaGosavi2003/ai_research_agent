# AI Research Assistant Agent

A modern full-stack web application demonstrating both **Generative AI** and **Agentic AI** concepts. The system executes a multi-step autonomous agent research pipeline, generating structured summaries, detailed technical explanations, interactive quizzes, interview preparation materials, and study roadmaps.

## 🚀 Key Features

* **User Authentication:** Session-based user sign-up, login, and secure session management.
* **Autonomous Research Agent:** An 8-step execution pipeline running query parsing, explanation, quiz creation, roadmaps, and more in real-time.
* **Server-Sent Events (SSE):** Live progress indicators showing step progression without frontend polling.
* **ChatGPT-Style Chat:** Continuous conversational interface to ask follow-up questions referencing previous report context.
* **Interactive Quizzes:** Dynamically generated multiple-choice tests with real-time feedback and detailed explanations.
* **ReportLab PDF Export:** Beautiful, automated PDF generation compiling the full report including page counts and dynamic headers.
* **Analytics Dashboard:** Graphical weekly research tracking (via Chart.js) and history records.
* **Theme Switching:** Premium glassmorphism design supporting both Dark and Light visual themes.

---

## 🛠️ Technology Stack

* **Frontend:** HTML5, CSS3 (Vanilla design tokens, CSS variables, transitions), Javascript (Vanilla, SSE, Chart.js)
* **Backend:** Python Flask
* **Database:** SQLite
* **AI Service:** Google Gemini Pro API (via `google-generativeai`)
* **PDF Engine:** ReportLab

---

## 📁 Project Directory Structure

```
ai_research_agent/
├── app.py                  # Server entrypoint & configuration setup
├── config.py               # Flask session and API credentials config
├── database.py             # SQLite helper and schema migrations
├── requirements.txt        # Package dependencies
├── INSTALLATION_GUIDE.md   # Setup instructions
├── PROJECT_REPORT.md       # Architectural overview
│
├── services/               # Core business services
│   ├── __init__.py
│   ├── ai_service.py       # Prompt engineering & mock fallback provider
│   └── pdf_service.py      # PDF document generator
│
├── routes/                 # Blueprint controllers
│   ├── __init__.py
│   ├── auth.py             # Login, register, logout controllers
│   ├── dashboard.py        # Analytics settings & history handlers
│   └── agent.py            # SSE streams, PDF exports & chatbot handles
│
├── static/                 # Static asset delivery
│   ├── css/
│   │   └── style.css       # Core styles (Variables, themes, responsive layout)
│   └── js/
│       ├── main.js         # Core layout helpers (Sidebar drawers, toasts)
│       └── agent.js        # SSE parsing, interactive quiz & chat loaders
│
└── templates/              # HTML layout views
    ├── base.html           # Main template outline
    ├── landing.html        # Product description landing screen
    ├── dashboard.html      # Stats dashboard overview
    ├── agent.html          # Interactive workspace & chat viewport
    └── auth/
        ├── login.html      # Sign-in viewport
        └── register.html   # Sign-up viewport
```

---

## 🏃 Quick Start

To run the application, navigate to this project folder, verify Python is installed, and execute:

```bash
python app.py
```

Open your browser to `http://127.0.0.1:5000` to begin.
For complete installation and API key configuration details, consult [INSTALLATION_GUIDE.md](file:///C:/Users/kerav/.gemini/antigravity-ide/scratch/ai_research_agent/INSTALLATION_GUIDE.md).
