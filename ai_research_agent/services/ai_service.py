import os
import time
import json
import google.generativeai as genai

# Setup Gemini SDK if API key is present
def configure_gemini(api_key):
    if api_key:
        genai.configure(api_key=api_key)
        return True
    return False

# ---------------------------------------------------------
# SIMULATION DATA FOR OUT-OF-THE-BOX OPERATION
# ---------------------------------------------------------

SIMULATED_REPORTS = {
    "cyber security": {
        "explanation": """<h3>Introduction to Cyber Security</h3>
<p>Cyber Security refers to the practice of protecting systems, networks, programs, devices, and data from cyber attacks, unauthorized access, or damage. As technology has become deeply integrated into business operations and daily lives, the surface area for potential attacks has increased exponentially.</p>
<p>Modern cyber security operates on multiple layers of protection spread across computers, networks, programs, or data. In any organization, the people, processes, and technology must all complement one another to create an effective defense against cyber threats.</p>
<h4>Core Pillars (The CIA Triad)</h4>
<ul>
  <li><strong>Confidentiality:</strong> Ensuring that data is accessible only to those authorized to have access. Enforced using encryption, access control lists, and multi-factor authentication.</li>
  <li><strong>Integrity:</strong> Guarding against improper information modification or destruction. Maintained using hashing algorithms, digital signatures, and version controls.</li>
  <li><strong>Availability:</strong> Ensuring timely and reliable access to and use of information. Maintained through server redundancy, backups, DDoS mitigation, and disaster recovery plans.</li>
</ul>""",
        "key_points": """<ul>
  <li><strong>Threat Landscape:</strong> Includes malware (viruses, ransomware, spyware), phishing, denial-of-service (DoS) attacks, SQL injection, and advanced persistent threats (APTs).</li>
  <li><strong>Zero Trust Architecture:</strong> A modern security framework built on the premise of "never trust, always verify" regardless of whether the request originates inside or outside the network perimeter.</li>
  <li><strong>Network Security:</strong> Protects traffic flow by controlling inbound and outbound connections via firewalls, Intrusion Detection/Prevention Systems (IDS/IPS), and VPNs.</li>
  <li><strong>Cryptography:</strong> The mathematical foundation of secure communications, split into symmetric (AES) and asymmetric (RSA, ECC) encryption.</li>
  <li><strong>Human Factor:</strong> Social engineering (phishing, baiting) remains the most common entry point for breaches, making regular security awareness training vital.</li>
</ul>""",
        "interview_questions": """<div class="qa-item">
  <div class="question">Q1: Explain the difference between Symmetric and Asymmetric Encryption.</div>
  <div class="answer"><strong>Answer:</strong> Symmetric encryption uses a single key for both encryption and decryption, making it fast but difficult to securely distribute keys. Examples include AES and DES. Asymmetric encryption uses a public key to encrypt and a private key to decrypt, solving key distribution issues at the cost of processing speed. Examples include RSA and ECC.</div>
</div>
<div class="qa-item">
  <div class="question">Q2: What is a Man-in-the-Middle (MitM) attack, and how do you prevent it?</div>
  <div class="answer"><strong>Answer:</strong> A MitM attack occurs when an attacker secretly intercepts and alters communication between two parties. Mitigation includes using HTTPS/TLS, implementing strict HSTS policies, using VPNs on untrusted networks, and verifying digital certificates.</div>
</div>
<div class="qa-item">
  <div class="question">Q3: What is the difference between Vulnerability Scanning and Penetration Testing?</div>
  <div class="answer"><strong>Answer:</strong> Vulnerability scanning is an automated, high-level tool-driven scan that identifies potential weaknesses in systems. Penetration testing is a hands-on, simulated cyber attack performed by a human specialist to actively exploit security vulnerabilities and assess real risk.</div>
</div>""",
        "quiz": """[
  {
    "question": "Which security concept ensures that information is not altered by unauthorized users?",
    "options": ["Confidentiality", "Integrity", "Availability", "Non-repudiation"],
    "answer": "Integrity",
    "explanation": "Integrity ensures data remains accurate and unaltered during storage or transit."
  },
  {
    "question": "What type of attack attempts to make server resources unavailable by flooding them with traffic?",
    "options": ["Phishing", "SQL Injection", "Distributed Denial of Service (DDoS)", "Buffer Overflow"],
    "answer": "Distributed Denial of Service (DDoS)",
    "explanation": "DDoS attacks saturate network bandwidth or server resources using botnets to disrupt service."
  },
  {
    "question": "Which protocol is used to securely browse websites by encrypting communications?",
    "options": ["HTTP", "FTP", "HTTPS", "SMTP"],
    "answer": "HTTPS",
    "explanation": "HTTPS runs HTTP over TLS/SSL to encrypt traffic between client and server."
  }
]""",
        "summary": "<p>Cyber Security is an essential, multi-dimensional discipline focused on protecting digital infrastructure and data assets. The threat landscape is constantly evolving, requiring organizations to transition from traditional perimeter security to adaptive, data-centric frameworks like Zero Trust. Ultimately, strong cyber security relies on combining robust engineering controls, organizational policies, and widespread user awareness.</p>",
        "roadmap": """<div class="roadmap-phase">
  <div class="phase-title">Phase 1: Foundations (Months 1-3)</div>
  <p>Learn networking basics (TCP/IP, OSI model), operating system administration (Linux command line, Windows Server), and fundamental security concepts.</p>
</div>
<div class="roadmap-phase">
  <div class="phase-title">Phase 2: Security Principles & Defensive Tools (Months 4-6)</div>
  <p>Study cryptography, firewalls, IDS/IPS tools, SIEM systems (Splunk), and identity access management. Gain certification like CompTIA Security+.</p>
</div>
<div class="roadmap-phase">
  <div class="phase-title">Phase 3: Specialty Specialization (Months 7-12)</div>
  <p>Choose a path: Ethical Hacking/Pentesting (CEH, OSCP) or Blue Teaming/SOC Analysis. Learn scripting (Python/Bash) for security automation.</p>
</div>""",
        "references_data": """<ul>
  <li><strong>Book:</strong> "Computer Networking: A Top-Down Approach" by Kurose & Ross - Essential for understanding network communications.</li>
  <li><strong>Portals:</strong> OWASP Foundation (owasp.org) - The industry authority on web application security standards.</li>
  <li><strong>Certifications:</strong> CompTIA Security+ & Offensive Security Certified Professional (OSCP) study guides.</li>
</ul>"""
    },
    "machine learning": {
        "explanation": """<h3>Introduction to Machine Learning</h3>
<p>Machine Learning (ML) is a subset of Artificial Intelligence (AI) focused on building systems that learn from data, identify patterns, and make decisions with minimal human intervention. Instead of writing explicit logic to solve a problem, developers feed examples to an algorithm, which constructs a statistical model to generalize rules.</p>
<h4>Core Categories of Machine Learning</h4>
<ul>
  <li><strong>Supervised Learning:</strong> The algorithm is trained on labeled training data. The model tries to map inputs to correct outputs. Examples: Linear Regression, Support Vector Machines (SVM), Decision Trees.</li>
  <li><strong>Unsupervised Learning:</strong> The model is trained on unlabeled data. It seeks to uncover hidden structures or groupings. Examples: K-Means Clustering, Principal Component Analysis (PCA).</li>
  <li><strong>Reinforcement Learning:</strong> An agent learns to make decisions by performing actions in an environment to maximize some cumulative reward. Examples: Q-Learning, Deep Q-Networks (DQN).</li>
</ul>""",
        "key_points": """<ul>
  <li><strong>Feature Engineering:</strong> The process of selecting, transforming, and extracting variables from raw data to improve model accuracy.</li>
  <li><strong>Overfitting vs. Underfitting:</strong> Overfitting occurs when a model learns training noise and fails to generalize to new data. Underfitting occurs when the model is too simple to capture the underlying structure.</li>
  <li><strong>Loss Functions & Optimization:</strong> Mathematical methods (like Gradient Descent) used to minimize errors during model training.</li>
  <li><strong>Evaluation Metrics:</strong> Precision, Recall, F1-Score, and Accuracy are critical metrics used to measure classifier performance.</li>
  <li><strong>Deep Learning:</strong> A subfield of ML utilizing multi-layered artificial neural networks inspired by the human brain to handle unstructured data (images, text).</li>
</ul>""",
        "interview_questions": """<div class="qa-item">
  <div class="question">Q1: What is the bias-variance tradeoff in Machine Learning?</div>
  <div class="answer"><strong>Answer:</strong> Bias is error due to overly simplistic assumptions in the learning algorithm (leads to underfitting). Variance is error due to high sensitivity to small fluctuations in the training set (leads to overfitting). The tradeoff refers to minimizing both errors simultaneously to create a generalized model.</div>
</div>
<div class="qa-item">
  <div class="question">Q2: How do you handle missing values in a dataset?</div>
  <div class="answer"><strong>Answer:</strong> Methods include dropping rows or columns with high missing rates, imputation using statistical metrics (mean, median, mode), predictive imputation (using another model to fill values), or using algorithms that handle missing values naturally (e.g., XGBoost).</div>
</div>
<div class="qa-item">
  <div class="question">Q3: What is Cross-Validation, and why is it used?</div>
  <div class="answer"><strong>Answer:</strong> Cross-validation (e.g., K-Fold) is a resampling technique that partitions data into subsets, training the model on some subsets while validating on others. It ensures the model does not overfit to a single train-test split.</div>
</div>""",
        "quiz": """[
  {
    "question": "What type of learning uses labeled input and output data?",
    "options": ["Supervised Learning", "Unsupervised Learning", "Reinforcement Learning", "Semi-supervised Clustering"],
    "answer": "Supervised Learning",
    "explanation": "Supervised learning relies on training datasets containing inputs along with correct target labels."
  },
  {
    "question": "Which of the following occurs when a model performs exceptionally well on training data but poorly on unseen data?",
    "options": ["Underfitting", "Overfitting", "Convergence", "Regularization"],
    "answer": "Overfitting",
    "explanation": "Overfitting is characterized by a model memorizing details and noise of training data, failing to generalize."
  },
  {
    "question": "Which optimization algorithm is commonly used to minimize the loss function of a neural network?",
    "options": ["K-Means", "Gradient Descent", "Principal Component Analysis", "Decision Tree"],
    "answer": "Gradient Descent",
    "explanation": "Gradient Descent is an iterative optimization algorithm used to find the minimum of a cost function by moving in the direction of steepest descent."
  }
]""",
        "summary": "<p>Machine Learning forms the backbone of modern data-driven software, shifting programming paradigms towards statistical modeling. Building effective ML pipelines involves not just fitting algorithms, but carefully collecting data, engineering features, and balancing bias and variance. The field is rapidly scaling, driven by Deep Learning architectures and cloud compute infrastructure.</p>",
        "roadmap": """<div class="roadmap-phase">
  <div class="phase-title">Phase 1: Mathematics & Python (Months 1-2)</div>
  <p>Master linear algebra, calculus, probability, and standard Python libraries (NumPy, Pandas, Matplotlib).</p>
</div>
<div class="roadmap-phase">
  <div class="phase-title">Phase 2: Classical Machine Learning (Months 3-5)</div>
  <p>Learn regression, classification, clustering, hyperparameter tuning, and Scikit-Learn libraries.</p>
</div>
<div class="roadmap-phase">
  <div class="phase-title">Phase 3: Deep Learning & Frameworks (Months 6-9)</div>
  <p>Study Neural Networks, CNNs, RNNs, and master TensorFlow or PyTorch. Learn MLOps concepts to deploy models.</p>
</div>""",
        "references_data": """<ul>
  <li><strong>Book:</strong> "Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow" by Aurélien Géron.</li>
  <li><strong>Online Courses:</strong> Machine Learning Specialization by Andrew Ng (Coursera).</li>
  <li><strong>Documentation:</strong> Scikit-Learn Official User Guide (scikit-learn.org).</li>
</ul>"""
    }
}

# ---------------------------------------------------------
# GEMINI API PROMPT ENGINEERING WRAPPERS
# ---------------------------------------------------------

def ask_gemini(prompt, api_key):
    """Utility to run a prompt through Gemini API."""
    try:
        if not api_key:
            return None
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text
        return None
    except Exception as e:
        print(f"Gemini API Error: {str(e)}")
        return None

def generate_explanation(topic, api_key=None):
    if not api_key:
        # Fallback to simulation
        normalized = topic.lower().strip()
        if normalized in SIMULATED_REPORTS:
            return SIMULATED_REPORTS[normalized]["explanation"]
        return f"""<h3>Detailed Explanation of {topic}</h3>
<p>This is a dynamically generated explanation for <strong>{topic}</strong>. The topic of {topic} is highly relevant in modern computing and technology ecosystems.</p>
<p>To understand {topic}, we must analyze its core components and architectural pillars. Many industries leverage {topic} to increase efficiency, guarantee security, and automate tedious manual processes. Implementing {topic} requires thorough analysis, robust frameworks, and compliance with industry standards.</p>
<h4>Key Concepts</h4>
<ul>
  <li><strong>Foundational Mechanics:</strong> The processes that form the baseline operations of {topic}.</li>
  <li><strong>Integration Paradigms:</strong> How {topic} connects with legacy systems and modern cloud architectures.</li>
  <li><strong>Security & Policy:</strong> Essential restrictions, data controls, and compliance rules associated with managing {topic}.</li>
</ul>"""

    prompt = f"""You are an expert technical researcher. 
Generate a detailed technical explanation of the topic: "{topic}".
Cover foundational concepts, architecture, design patterns, and why it is important.
Format the output in clean HTML (using tags like <h3>, <h4>, <p>, <ul>, <li>, <strong>). 
Do NOT wrap the response in ```html codeblocks. Return raw HTML content directly.
"""
    result = ask_gemini(prompt, api_key)
    return result or generate_explanation(topic, None)

def generate_key_points(topic, explanation_context, api_key=None):
    if not api_key:
        normalized = topic.lower().strip()
        if normalized in SIMULATED_REPORTS:
            return SIMULATED_REPORTS[normalized]["key_points"]
        return f"""<ul>
  <li><strong>Core Architecture:</strong> Dynamic workflows form the baseline architecture of {topic}.</li>
  <li><strong>Practical Scaling:</strong> Scaling {topic} is critical to achieving target operational throughput.</li>
  <li><strong>Automation Potential:</strong> Applying intelligence to {topic} significantly lowers manual oversight costs.</li>
  <li><strong>Security Considerations:</strong> Access vectors must be guarded closely to prevent vulnerabilities.</li>
  <li><strong>Industry Adaptability:</strong> Organizations across fintech, healthcare, and education are rapidly adopting {topic}.</li>
</ul>"""

    prompt = f"""Based on the topic "{topic}" and this explanation context:
{explanation_context[:1000]}

Generate 5 high-impact, technical key points (takeaways) summarizing the topic.
Format the output as a clean HTML bulleted list (<ul> and <li> tags).
Do NOT wrap the response in ```html. Return raw HTML content directly.
"""
    result = ask_gemini(prompt, api_key)
    return result or generate_key_points(topic, explanation_context, None)

def generate_interview_questions(topic, explanation_context, api_key=None):
    if not api_key:
        normalized = topic.lower().strip()
        if normalized in SIMULATED_REPORTS:
            return SIMULATED_REPORTS[normalized]["interview_questions"]
        return f"""<div class="qa-item">
  <div class="question">Q1: What are the fundamental prerequisites for implementing {topic}?</div>
  <div class="answer"><strong>Answer:</strong> Implementing {topic} requires robust infrastructure, skilled engineering resources, and a thorough assessment of existing architectural workflows. Clear baseline metrics must be defined to evaluate success.</div>
</div>
<div class="qa-item">
  <div class="question">Q2: Discuss the primary challenges associated with scaling {topic} in an enterprise system.</div>
  <div class="answer"><strong>Answer:</strong> Enterprise scaling challenges for {topic} include managing data consistency, latency issues, hardware limitations, security policy integration, and technical debt accumulated from legacy codebases.</div>
</div>
<div class="qa-item">
  <div class="question">Q3: How does security play a role in the deployment of {topic} systems?</div>
  <div class="answer"><strong>Answer:</strong> Security in {topic} requires implementing strong access control, encryption for transit and storage, regular auditing of logs, and adherence to the principle of least privilege.</div>
</div>"""

    prompt = f"""Generate 3-5 technical interview preparation questions with detailed answers for the topic: "{topic}".
Use this context:
{explanation_context[:1000]}

Format each question/answer in a clean block using HTML elements like:
<div class="qa-item">
  <div class="question">Q1: [Question here]</div>
  <div class="answer"><strong>Answer:</strong> [Detailed technical answer here]</div>
</div>
Do NOT wrap in codeblocks. Return raw HTML directly.
"""
    result = ask_gemini(prompt, api_key)
    return result or generate_interview_questions(topic, explanation_context, None)

def generate_quiz(topic, explanation_context, api_key=None):
    if not api_key:
        normalized = topic.lower().strip()
        if normalized in SIMULATED_REPORTS:
            return SIMULATED_REPORTS[normalized]["quiz"]
        # Fallback dynamic quiz JSON
        quiz_data = [
            {
                "question": f"Which of the following represents a primary component of {topic}?",
                "options": ["Standard Orchestration", "Redundant Storage", "Core Foundational Mechanics", "Distributed Caching"],
                "answer": "Core Foundational Mechanics",
                "explanation": f"Core Foundational Mechanics forms the base rules and patterns governing {topic} design."
            },
            {
                "question": f"What is a main bottleneck when deploying {topic} at enterprise scale?",
                "options": ["High latency", "Basic routing", "Excessive code comments", "Styling templates"],
                "answer": "High latency",
                "explanation": "High latency is a common issue when complex integrations require real-time synchronization."
            },
            {
                "question": f"How do teams ensure safety when processing datasets in {topic}?",
                "options": ["By ignoring logs", "By implementing End-to-End Encryption", "By reducing test coverage", "By running scripts manually"],
                "answer": "By implementing End-to-End Encryption",
                "explanation": "End-to-End Encryption secures data in transit and at rest, preventing unauthorized snooping."
            }
        ]
        return json.dumps(quiz_data)

    prompt = f"""Generate a multiple choice quiz for the topic "{topic}" in raw JSON array format.
Generate exactly 3 questions. Each item in the array must be a JSON object with:
- "question": string
- "options": list of 4 strings
- "answer": string matching exactly one of the options
- "explanation": string explaining why the answer is correct

Do NOT wrap the response in ```json or ``` codeblocks. Return only the raw JSON text.
Double check that the JSON is valid and parsable.
"""
    result = ask_gemini(prompt, api_key)
    if result:
        # Strip codeblock wrappers if Gemini added them despite instructions
        clean_result = result.strip()
        if clean_result.startswith("```"):
            clean_result = clean_result.split("\n", 1)[1]
            if clean_result.endswith("```"):
                clean_result = clean_result.rsplit("```", 1)[0]
        try:
            # Validate JSON
            parsed = json.loads(clean_result)
            return json.dumps(parsed)
        except Exception:
            pass
            
    # Default fallback if API fails or returns invalid JSON
    return generate_quiz(topic, explanation_context, None)

def generate_summary(topic, explanation_context, api_key=None):
    if not api_key:
        normalized = topic.lower().strip()
        if normalized in SIMULATED_REPORTS:
            return SIMULATED_REPORTS[normalized]["summary"]
        return f"<p>In summary, {topic} is a significant technical paradigm that dictates modern workflow structures. Mastering it involves understanding foundational dynamics and deploying strict security and performance metrics.</p><p>As technology marches forward, {topic} will continue to play an important role, adapting to serverless deployments, automated intelligence agents, and global scaling demands.</p>"

    prompt = f"""Based on the topic "{topic}" and this explanation context:
{explanation_context[:1000]}

Generate a concise, two-paragraph executive summary of the topic.
Format the output in clean HTML (<p> tags). Do NOT wrap in codeblocks.
"""
    result = ask_gemini(prompt, api_key)
    return result or generate_summary(topic, explanation_context, None)

def generate_roadmap(topic, explanation_context, api_key=None):
    if not api_key:
        normalized = topic.lower().strip()
        if normalized in SIMULATED_REPORTS:
            return SIMULATED_REPORTS[normalized]["roadmap"]
        return f"""<div class="roadmap-phase">
  <div class="phase-title">Phase 1: Concepts & Tools (Weeks 1-4)</div>
  <p>Learn core vocabulary, read introductory manuals, and setup basic development environments to experiment with {topic}.</p>
</div>
<div class="roadmap-phase">
  <div class="phase-title">Phase 2: Intermediate Scaling (Weeks 5-8)</div>
  <p>Understand integration patterns, APIs, performance metrics, and intermediate scripting controls.</p>
</div>
<div class="roadmap-phase">
  <div class="phase-title">Phase 3: Production Master (Weeks 9+)</div>
  <p>Focus on security audits, deployment strategies, continuous monitoring, and fault-tolerance mechanisms for {topic}.</p>
</div>"""

    prompt = f"""Create a clear step-by-step master roadmap for learning: "{topic}".
Divide it into 3 phases.
Format the output using HTML as follows:
<div class="roadmap-phase">
  <div class="phase-title">Phase 1: [Phase Name] ([Duration])</div>
  <p>[Detailed description of what to learn, milestones, and practices]</p>
</div>
...
Do NOT wrap in codeblocks. Return raw HTML directly.
"""
    result = ask_gemini(prompt, api_key)
    return result or generate_roadmap(topic, explanation_context, None)

def generate_references(topic, explanation_context, api_key=None):
    if not api_key:
        normalized = topic.lower().strip()
        if normalized in SIMULATED_REPORTS:
            return SIMULATED_REPORTS[normalized]["references_data"]
        return f"""<ul>
  <li><strong>Book:</strong> "Understanding {topic} in Depth" (Technical Press) - Great architectural guide.</li>
  <li><strong>Online Documentation:</strong> Official Standard Specifications for {topic} (spec.org).</li>
  <li><strong>Tutorial Portal:</strong> MasterClass tutorials on modern implementations of {topic}.</li>
</ul>"""

    prompt = f"""Suggest 3 high-quality references (books, online documentations, frameworks) to study "{topic}".
Format as a clean HTML bulleted list (<ul> and <li> tags) with bold titles.
Do NOT wrap in codeblocks.
"""
    result = ask_gemini(prompt, api_key)
    return result or generate_references(topic, explanation_context, None)

# ---------------------------------------------------------
# CHAT/CONVERSATION FOLLOW-UP SERVICE
# ---------------------------------------------------------

def answer_chat_followup(topic, report_content, chat_history, user_message, api_key=None):
    """
    Answers a follow-up user query about a researched topic within the ChatGPT-style interface.
    """
    if not api_key:
        # Simulate simple smart response
        return f"<p>Concerning your question: <em>\"{user_message}\"</em> in the context of <strong>{topic}</strong>.</p><p>As outlined in our research report, this is a common query. Typically, engineers resolve this by evaluating the performance tradeoffs, ensuring correct API scopes, and following security guidelines. Let me know if you would like me to clarify a specific point from the roadmap or quiz!</p>"

    # Build prompt with chat history context
    history_str = ""
    for msg in chat_history[-6:]:  # limit context to last 6 messages
        history_str += f"{msg['role'].capitalize()}: {msg['content']}\n"
        
    prompt = f"""You are a helpful AI Research Assistant. You recently compiled a research report on "{topic}".
    
The summary of the report is:
{report_content[:1500]}

Here is the conversation history with the user:
{history_str}
User: {user_message}

Provide a helpful, precise answer in clean HTML (<p>, <ul>, <li>, <strong>) addressing the user's question. 
Do NOT wrap in codeblocks.
"""
    result = ask_gemini(prompt, api_key)
    return result or answer_chat_followup(topic, report_content, chat_history, user_message, None)
