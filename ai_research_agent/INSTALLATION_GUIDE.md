# Installation Guide

Follow these steps to set up and run the AI Research Assistant Agent application on your local machine.

## Prerequisites

Ensure you have **Python 3.8+** installed on your system. You can verify this by running:

```bash
python --version
```

## Step 1: Clone or Open the Workspace

Ensure all project files are located inside your active project directory:
`C:\Users\kerav\.gemini\antigravity-ide\scratch\ai_research_agent\`

## Step 2: Install Dependencies

All required libraries are pre-installed in your agent environment. If you are setting up on a clean environment elsewhere, run:

```bash
pip install -r requirements.txt
```

### Required Packages:
* `Flask`
* `google-generativeai`
* `python-dotenv`
* `reportlab`
* `requests`

## Step 3: Configure environment variables (Optional)

The application will run automatically out-of-the-box in **Simulation Mode** if no API key is specified, allowing you to search topics like `Cyber Security` and `Machine Learning` instantly.

To connect the application to the live Gemini API, create a `.env` file in the root project directory:

```env
# C:\Users\kerav\.gemini\antigravity-ide\scratch\ai_research_agent\.env

SECRET_KEY=your-custom-session-secret-key
GEMINI_API_KEY=AIzaSy...YourActualGeminiAPIKeyHere
```

Alternatively, set it in your environment console before launching:
```powershell
$env:GEMINI_API_KEY="your_api_key"
```

## Step 4: Run the Application

Start the Flask server by running:

```bash
python app.py
```

By default, the server runs on `http://127.0.0.1:5000`. Open this URL in your web browser.

---

## 🧪 Verification Tasks

1. **User Sign Up:** Access the landing page, click **Get Started**, and register a new user.
2. **Launch Agent:** Search for `Cyber Security` or enter a custom topic to watch the progress timeline execute.
3. **Take a Quiz:** Go to the "Quiz" tab and click answers to test interactive quiz options.
4. **Follow-up Chat:** Submit follow-up questions in the Chat panel.
5. **Download PDF:** Click the PDF button to download a styled research summary document.
