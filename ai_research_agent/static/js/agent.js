/* ==========================================================================
   AI Research Assistant Agent - Agent Workspace Scripts
   ========================================================================== */

let sseSource = null;

// Sets search topic from badge list
function setTopic(topic) {
    const input = document.getElementById("topicInput");
    if (input) input.value = topic;
}

// Resets workspace back to initial search card
function resetWorkspace() {
    if (sseSource) {
        sseSource.close();
    }
    document.getElementById("reportWorkspaceCard").style.display = "none";
    document.getElementById("chatPanel").style.display = "none";
    document.getElementById("progressCard").style.display = "none";
    document.getElementById("searchCard").style.display = "block";
    
    // Clear inputs and history context
    document.getElementById("topicInput").value = "";
    window.currentSearchId = null;
    window.rawQuizData = null;
}

// Reset timeline items visually
function resetTimeline() {
    const steps = [1, 2, 3, 4, 5, 6, 7, 8];
    steps.forEach(s => {
        const item = document.getElementById(`step${s}`);
        const status = document.getElementById(`step${s}Status`);
        if (item && status) {
            item.className = "timeline-step";
            status.textContent = "Pending...";
            item.querySelector(".step-indicator").innerHTML = '<i data-lucide="circle"></i>';
        }
    });
    
    document.getElementById("progressBarFill").style.width = "0%";
    document.getElementById("progressPct").textContent = "0%";
    if (window.lucide) lucide.createIcons();
}

// Starts Server-Sent Events stream for multi-step agent execution
function startResearchStream() {
    const topicInput = document.getElementById("topicInput");
    const topic = topicInput.value.trim();
    
    if (!topic) {
        showToast("Please enter a research topic.", "error");
        return;
    }
    
    // Hide search card, show progress card
    document.getElementById("searchCard").style.display = "none";
    document.getElementById("progressCard").style.display = "block";
    document.getElementById("currentTargetTopic").textContent = topic;
    
    resetTimeline();
    
    const streamUrl = `/agent/run?topic=${encodeURIComponent(topic)}`;
    sseSource = new EventSource(streamUrl);
    
    sseSource.onmessage = function(event) {
        const payload = JSON.parse(event.data);
        const step = payload.step;
        const status = payload.status;
        const message = payload.message;
        const data = payload.data;
        const searchId = payload.search_id;

        // Update progress bar percentages
        if (step > 0 && step <= 8) {
            let pct = Math.round(((step - 1) / 8) * 100);
            if (status === "completed") {
                pct = Math.round((step / 8) * 100);
            }
            document.getElementById("progressBarFill").style.width = `${pct}%`;
            document.getElementById("progressPct").textContent = `${pct}%`;
        }

        if (status === "started") {
            const stepItem = document.getElementById(`step${step}`);
            const stepStatus = document.getElementById(`step${step}Status`);
            if (stepItem && stepStatus) {
                stepItem.classList.add("active");
                stepStatus.textContent = message;
                stepItem.querySelector(".step-indicator").innerHTML = '<i data-lucide="cpu" class="spinner"></i>';
                if (window.lucide) lucide.createIcons();
            }
        } 
        else if (status === "completed") {
            const stepItem = document.getElementById(`step${step}`);
            const stepStatus = document.getElementById(`step${step}Status`);
            if (stepItem && stepStatus) {
                stepItem.classList.remove("active");
                stepItem.classList.add("completed");
                stepStatus.textContent = message;
                stepItem.querySelector(".step-indicator").innerHTML = '<i data-lucide="check"></i>';
                if (window.lucide) lucide.createIcons();
            }
            
            // Populate content pane elements as they stream in
            populateStepContent(step, data);
        }
        else if (status === "finished") {
            document.getElementById("progressBarFill").style.width = "100%";
            document.getElementById("progressPct").textContent = "100%";
            
            showToast("Research compilation completed!", "success");
            sseSource.close();
            
            // Set global search parameters
            window.currentSearchId = searchId;
            document.getElementById("displayReportTopic").textContent = topic;
            
            // Update action URLs
            document.getElementById("downloadPdfBtn").href = `/agent/pdf/${searchId}`;
            
            // Transition workspace view
            setTimeout(() => {
                document.getElementById("progressCard").style.display = "none";
                document.getElementById("reportWorkspaceCard").style.display = "block";
                document.getElementById("chatPanel").style.display = "flex";
                
                // Clear chat panel messages and add welcome bubble
                const container = document.getElementById("chatMessagesContainer");
                container.innerHTML = `
                    <div class="chat-message assistant-message">
                        <div class="message-bubble">
                            <p>I have compiled the research report for <strong>${topic}</strong>. Feel free to ask any specific clarification or deep-dive questions, and I will assist you!</p>
                        </div>
                    </div>
                    <div class="chat-message assistant-message" id="chatTypingIndicator" style="display:none;">
                        <div class="message-bubble typing-bubble">
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                        </div>
                    </div>
                `;
                
                if (window.lucide) lucide.createIcons();
            }, 800);
        }
        else if (status === "error") {
            showToast(message, "error");
            sseSource.close();
            
            // Allow user to edit topic and retry
            setTimeout(() => {
                document.getElementById("progressCard").style.display = "none";
                document.getElementById("searchCard").style.display = "block";
            }, 1500);
        }
    };
    
    sseSource.onerror = function() {
        showToast("Connection to Research Agent stream lost.", "error");
        sseSource.close();
        
        setTimeout(() => {
            document.getElementById("progressCard").style.display = "none";
            document.getElementById("searchCard").style.display = "block";
        }, 1500);
    };
}

// Maps streaming steps to content placeholders
function populateStepContent(step, data) {
    if (!data) return;
    
    if (step === 2 && data.explanation) {
        document.getElementById("explanationContent").innerHTML = data.explanation;
    }
    else if (step === 3 && data.key_points) {
        document.getElementById("keyPointsContent").innerHTML = data.key_points;
    }
    else if (step === 4 && data.interview_questions) {
        document.getElementById("interviewContent").innerHTML = data.interview_questions;
    }
    else if (step === 5 && data.quiz) {
        window.rawQuizData = data.quiz;
        renderQuiz(data.quiz);
    }
    else if (step === 6 && data.summary) {
        document.getElementById("summaryContent").innerHTML = data.summary;
    }
    else if (step === 7 && data.roadmap) {
        document.getElementById("roadmapContent").innerHTML = data.roadmap;
    }
    else if (step === 8 && data.references_data) {
        document.getElementById("referencesContent").innerHTML = data.references_data;
    }
}

// Tab navigation handler
function switchTab(evt, tabId) {
    const tabPanes = document.getElementsByClassName("tab-pane");
    for (let i = 0; i < tabPanes.length; i++) {
        tabPanes[i].classList.remove("active");
    }
    
    const tabLinks = document.getElementsByClassName("tab-link");
    for (let i = 0; i < tabLinks.length; i++) {
        tabLinks[i].classList.remove("active");
    }
    
    document.getElementById(tabId).classList.add("active");
    evt.currentTarget.classList.add("active");
}

// Copies text inside report pane to clipboard
function copyPaneText(paneId) {
    const content = document.getElementById(paneId).querySelector(".pane-rich-content");
    if (!content) return;
    
    // Copy plaintext equivalent to clipboard
    const text = content.innerText;
    navigator.clipboard.writeText(text).then(() => {
        showToast("Section copied to clipboard!", "success");
    }).catch(err => {
        showToast("Failed to copy text.", "error");
    });
}

// ---------------------------------------------------------
/* Quiz Interactive Renderer */
// ---------------------------------------------------------
function renderQuiz(quizJson) {
    const quizContainer = document.getElementById("quizContent");
    if (!quizContainer) return;
    
    let questions = [];
    try {
        questions = typeof quizJson === "string" ? JSON.parse(quizJson) : quizJson;
    } catch (e) {
        quizContainer.innerHTML = "<p class='error-text'>Error parsing quiz content data.</p>";
        return;
    }
    
    if (!Array.isArray(questions) || questions.length === 0) {
        quizContainer.innerHTML = "<p>No practice quiz available for this topic.</p>";
        return;
    }
    
    let html = "<h3>Practice Assessment Quiz</h3>";
    
    questions.forEach((q, qIdx) => {
        html += `
            <div class="quiz-question-card" id="quizQ${qIdx}">
                <div class="quiz-q-title">Q${qIdx + 1}: ${escapeHtml(q.question)}</div>
                <div class="quiz-options-list">
        `;
        
        q.options.forEach((opt) => {
            html += `
                <button class="quiz-option-btn" onclick="selectQuizOption(this, ${qIdx}, '${escapeQuote(opt)}', '${escapeQuote(q.answer)}')">
                    ${escapeHtml(opt)}
                </button>
            `;
        });
        
        html += `
                </div>
                <div class="quiz-explanation-box" id="quizExp${qIdx}" style="display:none;">
                    <strong>Explanation:</strong> ${escapeHtml(q.explanation)}
                </div>
            </div>
        `;
    });
    
    quizContainer.innerHTML = html;
}

function selectQuizOption(btn, qIdx, selectedVal, correctVal) {
    const card = document.getElementById(`quizQ${qIdx}`);
    const buttons = card.querySelectorAll(".quiz-option-btn");
    
    // Disable all options in the card once choice is made
    buttons.forEach(b => {
        b.disabled = true;
        // Highlight correct option in green
        if (b.textContent.trim() === correctVal) {
            b.classList.add("correct");
        }
    });
    
    // If selected option was incorrect, highlight it red
    if (selectedVal !== correctVal) {
        btn.classList.add("incorrect");
        showToast("Incorrect answer. Read explanation below.", "error");
    } else {
        showToast("Correct answer! Good job.", "success");
    }
    
    // Reveal explanation block
    document.getElementById(`quizExp${qIdx}`).style.display = "block";
}

// ---------------------------------------------------------
/* Chat Follow-Up Submissions */
// ---------------------------------------------------------
function handleChatKeydown(e) {
    if (e.key === "Enter") {
        sendChatMessage();
    }
}

function sendChatMessage() {
    const input = document.getElementById("chatInput");
    const message = input.value.trim();
    if (!message || !window.currentSearchId) return;
    
    // Clear input field
    input.value = "";
    
    const container = document.getElementById("chatMessagesContainer");
    const indicator = document.getElementById("chatTypingIndicator");
    
    // Render user message bubble
    const userMsgDiv = document.createElement("div");
    userMsgDiv.className = "chat-message user-message";
    userMsgDiv.innerHTML = `
        <div class="message-bubble">
            <p>${escapeHtml(message)}</p>
        </div>
    `;
    container.insertBefore(userMsgDiv, indicator);
    scrollToBottom(container);
    
    // Show typing bubble
    indicator.style.display = "flex";
    scrollToBottom(container);
    
    // Post message to backend
    fetch("/agent/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            search_id: window.currentSearchId,
            message: message
        })
    })
    .then(res => res.json())
    .then(data => {
        indicator.style.display = "none";
        if (data.status === "success") {
            const assistantMsgDiv = document.createElement("div");
            assistantMsgDiv.className = "chat-message assistant-message";
            assistantMsgDiv.innerHTML = `
                <div class="message-bubble">
                    ${data.reply}
                </div>
            `;
            container.insertBefore(assistantMsgDiv, indicator);
            scrollToBottom(container);
        } else {
            showToast("Failed to fetch response.", "error");
        }
    })
    .catch(err => {
        indicator.style.display = "none";
        showToast("Error communicating with agent.", "error");
        console.error(err);
    });
}

// ---------------------------------------------------------
/* String sanitizing utilities */
// ---------------------------------------------------------
function escapeHtml(text) {
    if (!text) return "";
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

function escapeQuote(text) {
    if (!text) return "";
    return text.replace(/'/g, "\\'");
}

function scrollToBottom(el) {
    el.scrollTop = el.scrollHeight;
}
