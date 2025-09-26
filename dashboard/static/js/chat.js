/**
 * Modern Chat Interface with MCP Integration
 * Handles file uploads, agent communication, and real-time updates
 */

class ConfigResearchChat {
    constructor() {
        this.uploadedFiles = [];
        this.isProcessing = false;
        this.chatHistory = [];
        this.currentSessionId = this.generateSessionId();
        
        this.initializeElements();
        this.bindEvents();
        this.loadChatHistory();
    }

    initializeElements() {
        // Main elements
        this.chatContainer = document.querySelector('.chat-container');
        this.chatMessages = document.querySelector('.chat-messages');
        this.messageInput = document.querySelector('.message-input');
        this.sendButton = document.querySelector('.send-button');
        this.fileUploadArea = document.querySelector('.file-upload-area');
        this.uploadedFilesContainer = document.querySelector('.uploaded-files');
        this.inputForm = document.querySelector('.input-form');
        
        // File input (hidden)
        this.fileInput = document.createElement('input');
        this.fileInput.type = 'file';
        this.fileInput.multiple = true;
        this.fileInput.accept = '.xlsx,.xls,.pdf,.json,.yaml,.yml,.txt';
        this.fileInput.style.display = 'none';
        document.body.appendChild(this.fileInput);
    }

    bindEvents() {
        // Send message
        this.sendButton.addEventListener('click', () => this.sendMessage());
        this.messageInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // File upload
        this.fileUploadArea.addEventListener('click', () => this.fileInput.click());
        this.fileUploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.fileUploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.fileUploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

        // Auto-resize textarea
        this.messageInput.addEventListener('input', () => this.autoResizeTextarea());
    }

    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    autoResizeTextarea() {
        this.messageInput.style.height = 'auto';
        this.messageInput.style.height = Math.min(this.messageInput.scrollHeight, 8 * 16) + 'px';
    }

    handleDragOver(e) {
        e.preventDefault();
        this.fileUploadArea.classList.add('dragover');
    }

    handleDragLeave(e) {
        e.preventDefault();
        this.fileUploadArea.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.fileUploadArea.classList.remove('dragover');
        const files = Array.from(e.dataTransfer.files);
        this.processFiles(files);
    }

    handleFileSelect(e) {
        const files = Array.from(e.target.files);
        this.processFiles(files);
        e.target.value = ''; // Reset input
    }

    processFiles(files) {
        files.forEach(file => {
            if (this.validateFile(file)) {
                this.uploadFile(file);
            }
        });
    }

    validateFile(file) {
        const allowedTypes = [
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
            'application/vnd.ms-excel', // .xls
            'application/pdf',
            'application/json',
            'text/yaml',
            'text/x-yaml',
            'text/plain'
        ];

        const allowedExtensions = ['.xlsx', '.xls', '.pdf', '.json', '.yaml', '.yml', '.txt'];
        const fileExtension = '.' + file.name.split('.').pop().toLowerCase();

        if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
            this.showNotification('Invalid file type. Please upload Excel, PDF, JSON, YAML, or text files.', 'error');
            return false;
        }

        if (file.size > 10 * 1024 * 1024) { // 10MB limit
            this.showNotification('File size too large. Please upload files smaller than 10MB.', 'error');
            return false;
        }

        return true;
    }

    async uploadFile(file) {
        const fileId = this.generateFileId();
        const fileData = {
            id: fileId,
            name: file.name,
            size: file.size,
            type: file.type,
            file: file,
            status: 'uploading'
        };

        this.uploadedFiles.push(fileData);
        this.renderUploadedFiles();

        try {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('session_id', this.currentSessionId);

            const response = await fetch('/api/upload/file', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const result = await response.json();
                fileData.status = 'uploaded';
                fileData.serverPath = result.file_path;
                fileData.processedData = result.processed_data;
                this.showNotification(`File "${file.name}" uploaded successfully`, 'success');
            } else {
                throw new Error('Upload failed');
            }
        } catch (error) {
            fileData.status = 'error';
            this.showNotification(`Failed to upload "${file.name}"`, 'error');
        }

        this.renderUploadedFiles();
    }

    generateFileId() {
        return 'file_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    renderUploadedFiles() {
        this.uploadedFilesContainer.innerHTML = '';

        this.uploadedFiles.forEach(fileData => {
            const fileElement = document.createElement('div');
            fileElement.className = 'uploaded-file';
            fileElement.innerHTML = `
                <span class="file-icon">${this.getFileIcon(fileData.type)}</span>
                <span class="file-name">${fileData.name}</span>
                <span class="file-size">${this.formatFileSize(fileData.size)}</span>
                <span class="status-indicator ${fileData.status}">${fileData.status}</span>
                <button class="remove-file" onclick="chat.removeFile('${fileData.id}')">×</button>
            `;
            this.uploadedFilesContainer.appendChild(fileElement);
        });
    }

    getFileIcon(fileType) {
        if (fileType.includes('excel') || fileType.includes('spreadsheet')) {
            return '📊';
        } else if (fileType.includes('pdf')) {
            return '📄';
        } else if (fileType.includes('json')) {
            return '📋';
        } else if (fileType.includes('yaml')) {
            return '⚙️';
        } else {
            return '📁';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    removeFile(fileId) {
        this.uploadedFiles = this.uploadedFiles.filter(file => file.id !== fileId);
        this.renderUploadedFiles();
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        if (!message && this.uploadedFiles.length === 0) {
            this.showNotification('Please enter a message or upload files', 'warning');
            return;
        }

        if (this.isProcessing) {
            this.showNotification('Please wait for the current request to complete', 'warning');
            return;
        }

        // Add user message to chat
        this.addMessage('user', message, this.uploadedFiles);
        
        // Clear input and files
        this.messageInput.value = '';
        this.autoResizeTextarea();
        const filesToProcess = [...this.uploadedFiles];
        this.uploadedFiles = [];
        this.renderUploadedFiles();

        // Show processing indicator
        this.setProcessing(true);
        this.addProcessingIndicator();

        try {
            // Send request to agent
            const response = await this.sendToAgent(message, filesToProcess);
            
            // Remove processing indicator
            this.removeProcessingIndicator();
            
            // Add agent response
            this.addMessage('assistant', response.message, [], response.attachments, response.metadata);
            
        } catch (error) {
            this.removeProcessingIndicator();
            this.addMessage('assistant', 'Sorry, I encountered an error processing your request. Please try again.', [], [], { error: error.message });
            console.error('Error:', error);
        } finally {
            this.setProcessing(false);
        }
    }

    async sendToAgent(message, files) {
        const requestData = {
            session_id: this.currentSessionId,
            message: message,
            files: files.map(file => ({
                id: file.id,
                name: file.name,
                type: file.type,
                server_path: file.serverPath,
                processed_data: file.processedData
            }))
        };

        const response = await fetch('/api/chat/agent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    addMessage(sender, content, files = [], attachments = [], metadata = {}) {
        const messageId = this.generateMessageId();
        const timestamp = new Date().toLocaleTimeString();
        
        const messageData = {
            id: messageId,
            sender: sender,
            content: content,
            files: files,
            attachments: attachments,
            metadata: metadata,
            timestamp: timestamp
        };

        this.chatHistory.push(messageData);
        this.renderMessage(messageData);
        this.saveChatHistory();
    }

    generateMessageId() {
        return 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    renderMessage(messageData) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${messageData.sender}`;
        messageElement.id = messageData.id;

        const avatar = messageData.sender === 'user' ? '👤' : '🤖';
        const senderName = messageData.sender === 'user' ? 'You' : 'Configuration Agent';

        let filesHtml = '';
        if (messageData.files && messageData.files.length > 0) {
            filesHtml = '<div class="attached-files">';
            messageData.files.forEach(file => {
                filesHtml += `
                    <div class="file-attachment">
                        <span class="file-icon">${this.getFileIcon(file.type)}</span>
                        <span class="file-name">${file.name}</span>
                    </div>
                `;
            });
            filesHtml += '</div>';
        }

        let attachmentsHtml = '';
        if (messageData.attachments && messageData.attachments.length > 0) {
            attachmentsHtml = '<div class="attached-files">';
            messageData.attachments.forEach(attachment => {
                attachmentsHtml += `
                    <div class="file-attachment">
                        <span class="file-icon">${attachment.icon || '📎'}</span>
                        <span class="file-name">${attachment.name}</span>
                        <span class="file-size">${attachment.description || ''}</span>
                    </div>
                `;
            });
            attachmentsHtml += '</div>';
        }

        messageElement.innerHTML = `
            <div class="message-avatar">${avatar}</div>
            <div class="message-content">
                <div class="message-bubble">
                    ${this.formatMessageContent(messageData.content)}
                    ${filesHtml}
                    ${attachmentsHtml}
                </div>
                <div class="message-time">${messageData.timestamp}</div>
            </div>
        `;

        this.chatMessages.appendChild(messageElement);
        this.scrollToBottom();
    }

    formatMessageContent(content) {
        // Convert markdown-like formatting to HTML
        return content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    addProcessingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'processing-indicator';
        indicator.id = 'processing-indicator';
        indicator.innerHTML = `
            <div class="spinner"></div>
            <span>Processing your request...</span>
        `;
        this.chatMessages.appendChild(indicator);
        this.scrollToBottom();
    }

    removeProcessingIndicator() {
        const indicator = document.getElementById('processing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    setProcessing(processing) {
        this.isProcessing = processing;
        this.sendButton.disabled = processing;
        this.sendButton.textContent = processing ? 'Processing...' : 'Send';
        
        if (processing) {
            this.sendButton.innerHTML = '<div class="spinner"></div> Processing...';
        } else {
            this.sendButton.innerHTML = 'Send';
        }
    }

    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${this.getNotificationIcon(type)}</span>
                <span class="notification-message">${message}</span>
            </div>
        `;

        // Add to page
        document.body.appendChild(notification);

        // Show notification
        setTimeout(() => notification.classList.add('show'), 100);

        // Remove notification
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    getNotificationIcon(type) {
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        return icons[type] || icons.info;
    }

    saveChatHistory() {
        localStorage.setItem('config_research_chat_history', JSON.stringify(this.chatHistory));
    }

    loadChatHistory() {
        const saved = localStorage.getItem('config_research_chat_history');
        if (saved) {
            try {
                this.chatHistory = JSON.parse(saved);
                this.chatHistory.forEach(message => this.renderMessage(message));
                this.scrollToBottom();
            } catch (error) {
                console.error('Error loading chat history:', error);
                this.chatHistory = [];
            }
        }
    }

    clearChatHistory() {
        this.chatHistory = [];
        this.chatMessages.innerHTML = '';
        localStorage.removeItem('config_research_chat_history');
        this.showNotification('Chat history cleared', 'success');
    }

    sendQuickMessage(message) {
        this.messageInput.value = message;
        this.autoResizeTextarea();
        this.sendMessage();
    }
}

// Initialize chat when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.chat = new ConfigResearchChat();
});

// Add notification styles
const notificationStyles = `
    .notification {
        position: fixed;
        top: 1rem;
        right: 1rem;
        background: white;
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
        padding: 1rem;
        z-index: 1000;
        transform: translateX(100%);
        transition: transform 0.3s ease-out;
        max-width: 300px;
    }

    .notification.show {
        transform: translateX(0);
    }

    .notification-content {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .notification-icon {
        font-size: 1.25rem;
    }

    .notification-message {
        font-size: 0.875rem;
        color: var(--text-primary);
    }

    .notification-success {
        border-left: 4px solid var(--success-color);
    }

    .notification-error {
        border-left: 4px solid var(--error-color);
    }

    .notification-warning {
        border-left: 4px solid var(--warning-color);
    }

    .notification-info {
        border-left: 4px solid var(--primary-color);
    }
`;

// Add styles to head
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);