// API Configuration
const API_URL = 'http://localhost:8000';

// Global State
let bookId = null;
let sessionId = null;
let currentMode = 'normal';

// Toggle chat widget open/close
function toggleChat() {
    const widget = document.getElementById('chatWidget');
    const button = document.getElementById('chatButton');
    const badge = document.getElementById('notificationBadge');

    widget.classList.toggle('open');
    button.classList.toggle('active');

    // Hide notification badge when opened
    if (widget.classList.contains('open')) {
        badge.classList.add('hidden');
    }
}

// Show/Hide loading spinner
function showLoading() {
    document.getElementById('loadingSpinner').style.display = 'block';
}

function hideLoading() {
    document.getElementById('loadingSpinner').style.display = 'none';
}

// Show upload status
function showUploadStatus(message, type = 'success') {
    const statusDiv = document.getElementById('uploadStatusWidget');
    statusDiv.textContent = message;
    statusDiv.className = 'upload-status ' + type;
}

// Handle file selection
function handleFileSelect() {
    const fileInput = document.getElementById('bookFileWidget');
    const uploadBtn = document.getElementById('uploadBtnWidget');

    if (fileInput.files.length > 0) {
        const fileName = fileInput.files[0].name;
        showUploadStatus(`Selected: ${fileName}`, 'processing');
        uploadBtn.style.display = 'block';
    }
}

// Upload book
async function uploadBookWidget() {
    const fileInput = document.getElementById('bookFileWidget');
    const file = fileInput.files[0];

    if (!file) {
        showUploadStatus('Please select a file first!', 'error');
        return;
    }

    // Validate file type
    const allowedTypes = ['.pdf', '.html', '.htm', '.epub'];
    const fileName = file.name.toLowerCase();
    const isAllowed = allowedTypes.some(ext => fileName.endsWith(ext));

    if (!isAllowed) {
        showUploadStatus('Only PDF, HTML, EPUB files are supported!', 'error');
        return;
    }

    showLoading();
    showUploadStatus('Processing book... This may take 1-2 minutes...', 'processing');

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_URL}/ingest/book`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.status === 'completed') {
            bookId = data.book_id;
            showUploadStatus(`✓ Book uploaded! ${data.total_chunks} chunks created.`, 'success');

            // Switch to chat interface after 1 second
            setTimeout(() => {
                document.getElementById('uploadSectionWidget').style.display = 'none';
                document.getElementById('chatMessagesSection').style.display = 'flex';
            }, 1000);
        } else {
            showUploadStatus(`Error: ${data.message || 'Upload failed'}`, 'error');
        }

    } catch (error) {
        showUploadStatus(`Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Switch between normal and selection mode
function switchModeWidget(mode) {
    currentMode = mode;

    // Update tabs
    document.getElementById('normalTab').classList.toggle('active', mode === 'normal');
    document.getElementById('selectionTab').classList.toggle('active', mode === 'selection');

    // Show/hide sections
    document.getElementById('normalChatWidget').style.display = mode === 'normal' ? 'block' : 'none';
    document.getElementById('selectionChatWidget').style.display = mode === 'selection' ? 'block' : 'none';
}

// Add message to chat
function addMessageWidget(content, isUser = false, sources = null) {
    const messagesDiv = document.getElementById('chatMessagesWidget');

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

    let messageHTML = `<div class="message-content">${escapeHtml(content)}`;

    // Add sources if available
    if (sources && sources.length > 0) {
        messageHTML += `<div class="source-info"><strong>📚 Sources:</strong><br>`;
        sources.slice(0, 2).forEach((source, idx) => {
            messageHTML += `
                <div class="source-chunk">
                    <strong>Chunk ${idx + 1}</strong> (${source.score.toFixed(2)})<br>
                    ${escapeHtml(source.text.substring(0, 80))}...
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

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Send message (normal chat)
async function sendMessageWidget() {
    const input = document.getElementById('userInputWidget');
    const message = input.value.trim();

    if (!message) return;
    if (!bookId) {
        alert('Book is still processing. Please wait...');
        return;
    }

    // Add user message
    addMessageWidget(message, true);
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
            addMessageWidget(data.response, false, data.sources);
        } else {
            addMessageWidget(`Error: ${data.detail || 'Failed to get response'}`, false);
        }

    } catch (error) {
        addMessageWidget(`Error: ${error.message}`, false);
    } finally {
        hideLoading();
    }
}

// Ask about selected text
async function askSelectionWidget() {
    const selectedText = document.getElementById('selectedTextWidget').value.trim();
    const question = document.getElementById('selectionQuestionWidget').value.trim();

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
            const responseDiv = document.getElementById('selectionResponseWidget');
            responseDiv.innerHTML = `
                <strong>Q:</strong> ${escapeHtml(question)}<br><br>
                <strong>A:</strong> ${escapeHtml(data.response)}
            `;
            responseDiv.classList.add('show');

            // Clear question input
            document.getElementById('selectionQuestionWidget').value = '';
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
function handleKeyPressWidget(event) {
    if (event.key === 'Enter') {
        sendMessageWidget();
    }
}

// Handle Enter key in selection mode
function handleSelectionKeyPressWidget(event) {
    if (event.key === 'Enter') {
        askSelectionWidget();
    }
}

// Initialize - show notification badge on page load
window.addEventListener('load', () => {
    // Optional: Auto-open chat after 3 seconds
    // setTimeout(() => {
    //     if (!document.getElementById('chatWidget').classList.contains('open')) {
    //         toggleChat();
    //     }
    // }, 3000);
});
