// API base URL
const API_URL = 'http://localhost:8000';

// Global state
let bookId = null;
let sessionId = null;
let currentMode = 'normal';  // 'normal' or 'selection'

// Show/Hide loading overlay
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

// Show status message
function showStatus(message, isError = false) {
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.textContent = message;
    statusDiv.className = 'status-message ' + (isError ? 'error' : 'success');
}

// Upload book
async function uploadBook() {
    const fileInput = document.getElementById('bookFile');
    const file = fileInput.files[0];

    if (!file) {
        showStatus('Please select a file first!', true);
        return;
    }

    // Check file type
    const allowedTypes = ['.pdf', '.html', '.htm', '.epub'];
    const fileName = file.name.toLowerCase();
    const isAllowed = allowedTypes.some(ext => fileName.endsWith(ext));

    if (!isAllowed) {
        showStatus('Only PDF, HTML, EPUB files are supported!', true);
        return;
    }

    showLoading();

    try {
        // Create FormData
        const formData = new FormData();
        formData.append('file', file);

        // Upload to API
        const response = await fetch(`${API_URL}/ingest/book`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.status === 'completed') {
            bookId = data.book_id;
            showStatus(`✓ Book uploaded successfully! ${data.total_chunks} chunks created.`);

            // Show chat section
            document.getElementById('chatSection').style.display = 'block';

            // Scroll to chat section
            document.getElementById('chatSection').scrollIntoView({ behavior: 'smooth' });
        } else {
            showStatus(`Error: ${data.message || 'Upload failed'}`, true);
        }

    } catch (error) {
        showStatus(`Error: ${error.message}`, true);
    } finally {
        hideLoading();
    }
}

// Switch between normal and selection mode
function switchMode(mode) {
    currentMode = mode;

    // Update button states
    document.getElementById('normalModeBtn').classList.toggle('active', mode === 'normal');
    document.getElementById('selectionModeBtn').classList.toggle('active', mode === 'selection');

    // Show/hide sections
    document.getElementById('normalChatMode').style.display = mode === 'normal' ? 'block' : 'none';
    document.getElementById('selectionChatMode').style.display = mode === 'selection' ? 'block' : 'none';
}

// Add message to chat
function addMessage(content, isUser = false, sources = null) {
    const messagesDiv = document.getElementById('chatMessages');

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

    let messageHTML = `<div class="message-content">${content}`;

    // Add sources if available
    if (sources && sources.length > 0) {
        messageHTML += `<div class="source-info"><strong>📚 Sources:</strong>`;
        sources.forEach((source, idx) => {
            messageHTML += `
                <div class="source-chunk">
                    <strong>Chunk ${idx + 1}</strong> (score: ${source.score.toFixed(3)})<br>
                    ${source.text.substring(0, 150)}...
                </div>
            `;
        });
        messageHTML += `</div>`;
    }

    messageHTML += `</div>`;
    messageDiv.innerHTML = messageHTML;

    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Send message (normal chat)
async function sendMessage() {
    const input = document.getElementById('userInput');
    const message = input.value.trim();

    if (!message) return;
    if (!bookId) {
        alert('Please upload a book first!');
        return;
    }

    // Add user message
    addMessage(message, true);
    input.value = '';

    showLoading();

    try {
        const response = await fetch(`${API_URL}/chat/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                book_id: bookId,
                message: message,
                session_id: sessionId
            })
        });

        const data = await response.json();

        if (response.ok) {
            sessionId = data.session_id;
            addMessage(data.response, false, data.sources);
        } else {
            addMessage(`Error: ${data.detail || 'Failed to get response'}`, false);
        }

    } catch (error) {
        addMessage(`Error: ${error.message}`, false);
    } finally {
        hideLoading();
    }
}

// Ask about selected text
async function askSelection() {
    const selectedText = document.getElementById('selectedText').value.trim();
    const question = document.getElementById('selectionQuestion').value.trim();

    if (!selectedText || !question) {
        alert('Please provide both selected text and question!');
        return;
    }

    if (selectedText.length > 10000) {
        alert('Selected text is too long! Maximum 10000 characters.');
        return;
    }

    showLoading();

    try {
        const response = await fetch(`${API_URL}/chat/selection`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                selected_text: selectedText,
                question: question,
                session_id: sessionId
            })
        });

        const data = await response.json();

        if (response.ok) {
            sessionId = data.session_id;

            // Show response
            const responseDiv = document.getElementById('selectionResponse');
            responseDiv.innerHTML = `
                <strong>Question:</strong> ${question}<br><br>
                <strong>Answer:</strong><br>${data.response}
            `;
            responseDiv.classList.add('show');

            // Clear question input
            document.getElementById('selectionQuestion').value = '';
        } else {
            alert(`Error: ${data.detail || 'Failed to get response'}`);
        }

    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        hideLoading();
    }
}

// Handle Enter key in normal chat
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Handle Enter key in selection mode
function handleSelectionKeyPress(event) {
    if (event.key === 'Enter') {
        askSelection();
    }
}
