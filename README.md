# AI Research Assistant Agent

## Overview

AI Research Assistant Agent is a full-stack web application that demonstrates the concepts of **Generative AI** and **Agentic AI**. The application accepts a user-provided topic and automatically performs a sequence of AI-driven tasks to generate comprehensive learning material, including explanations, summaries, interview questions, quizzes, learning roadmaps, and downloadable reports.

The project showcases how multiple AI agents can collaborate to complete a complex workflow while providing an intuitive and responsive user experience.

---

## Features

* User authentication (Register, Login, Logout)
* AI-powered research assistant
* Detailed topic explanation
* Key point extraction
* Automatic summary generation
* Interview question generation
* Multiple-choice quiz generation with answers
* Learning roadmap generation
* Reference and resource recommendations
* Chat-based interface
* Search history management
* PDF report export
* Dark and Light theme support
* Responsive design for desktop and mobile devices

---

## Technology Stack

**Frontend**

* HTML
* CSS
* JavaScript

**Backend**

* Python
* Flask

**Database**

* SQLite

**Artificial Intelligence**

* Google Gemini API

**Report Generation**

* ReportLab / FPDF

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/AI-Research-Assistant-Agent.git
```

Navigate to the project directory:

```bash
cd AI-Research-Assistant-Agent
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python app.py
```

Open the application in your browser:

```
http://127.0.0.1:5000
```

---

## Project Structure

```text
AI-Research-Assistant-Agent/
│
├── app.py
├── requirements.txt
├── README.md
├── database/
├── models/
├── routes/
├── services/
├── static/
│   ├── css/
│   ├── js/
│   └── images/
├── templates/
└── reports/
```

---

## Agent Workflow

The application follows a structured multi-agent workflow:

1. Analyze the user's query.
2. Generate a detailed explanation.
3. Extract the main concepts.
4. Generate interview questions.
5. Create a multiple-choice quiz with answers.
6. Produce a concise summary.
7. Recommend a learning roadmap.
8. Suggest additional learning resources.
9. Export the generated report as a PDF.

---

## Use Cases

* Academic research
* Student learning
* Technical interview preparation
* Internship demonstrations
* Self-paced learning
* Topic exploration

---

## Future Enhancements

* Voice interaction
* Multi-language support
* Document upload and analysis
* Retrieval-Augmented Generation (RAG)
* Team collaboration features
* Cloud database integration
* Email report sharing

---

## Contributing

Contributions are welcome. If you would like to improve the project, please fork the repository, create a feature branch, and submit a pull request.

---

## License

This project is licensed under the MIT License.

---

## Author

**Chaitanya Gosavi**

Developed as part of the **Generative AI & Agentic Systems Engineering Internship**.
