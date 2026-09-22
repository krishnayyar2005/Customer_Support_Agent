const API_BASE_URL = "http://localhost:8080";

document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const chatForm = document.getElementById('chat-form');
  const chatInput = document.getElementById('chat-input');
  const sendBtn = document.getElementById('send-btn');
  const clearBtn = document.getElementById('clear-btn');
  const chatMessagesContainer = document.getElementById('chat-messages-container');
  
  const emptyState = document.getElementById('empty-state');
  const loadingIndicator = document.getElementById('loading-indicator');
  const errorState = document.getElementById('error-state');
  const errorDesc = document.getElementById('error-desc');
  const retryBtn = document.getElementById('retry-btn');
  
  const suggestionCards = document.querySelectorAll('.suggestion-card');

  // State
  let conversationId = null;
  let isLoading = false;
  let lastFailedMessage = null;
  let messages = []; // shadow array for localStorage persistence

  const STORAGE_KEY = 'reliance_chat_state';

  // ── localStorage helpers ──────────────────────────────────────
  const saveChatState = () => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify({
        conversationId,
        messages
      }));
    } catch (_) { /* quota exceeded or private mode – ignore */ }
  };

  const clearChatState = () => {
    try { localStorage.removeItem(STORAGE_KEY); } catch (_) {}
  };

  const restoreChatState = () => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return false;
      const state = JSON.parse(raw);
      if (!state || !Array.isArray(state.messages) || state.messages.length === 0) return false;

      conversationId = state.conversationId || null;
      messages = state.messages;

      hideEmptyState();
      messages.forEach(msg => {
        if (msg.role === 'user') {
          renderMessageBubble('user', msg.text, msg.timestamp);
        } else if (msg.role === 'assistant') {
          renderMessageBubble('assistant', msg.text, msg.timestamp);
        }
      });
      scrollToBottom();
      return true;
    } catch (_) {
      // corrupted value – wipe it and fall back to empty state
      clearChatState();
      return false;
    }
  };

  // Helpers
  const formatTime = () => new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  
  const scrollToBottom = () => {
    chatMessagesContainer.scrollTop = chatMessagesContainer.scrollHeight;
  };

  const setInputState = (disabled) => {
    chatInput.disabled = disabled;
    sendBtn.disabled = disabled || !chatInput.value.trim();
  };

  // UI rendering
  const hideEmptyState = () => {
    if (emptyState && !emptyState.classList.contains('hidden')) {
      emptyState.classList.add('hidden');
    }
  };

  // Low-level render that accepts an explicit timestamp (used by both
  // live messages and restore-from-localStorage).
  const renderMessageBubble = (role, text, time) => {
    let html;
    if (role === 'user') {
      html = `
        <div class="msg-user animate-fade-in">
          <div style="display: flex; flexDirection: column; align-items: flex-end; gap: 4px;">
            <div class="user-bubble">
              <p class="text-body-md" style="color: var(--on-tertiary);">${escapeHtml(text)}</p>
            </div>
            <div class="msg-meta-user">
              <span class="text-label-sm" style="color: var(--on-surface-variant);">${time}</span>
              <span class="material-symbols-outlined" style="font-size: 14px; color: var(--secondary);">done_all</span>
            </div>
          </div>
        </div>`;
    } else {
      html = `
        <div class="msg-agent animate-fade-in">
          <div class="agent-avatar">
            <span class="material-symbols-outlined" style="font-size: 18px;">support_agent</span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 4px;">
            <div class="agent-bubble">
              <p class="text-body-md" style="white-space: pre-wrap;">${escapeHtml(text)}</p>
            </div>
            <span class="text-label-sm msg-meta">${time} • resQ Virtual Specialist</span>
          </div>
        </div>`;
    }
    loadingIndicator.insertAdjacentHTML('beforebegin', html);
  };

  const renderUserMessage = (text) => {
    const time = formatTime();
    renderMessageBubble('user', text, time);
    messages.push({ role: 'user', text, timestamp: time });
    saveChatState();
    scrollToBottom();
  };

  const renderAgentMessage = (text) => {
    const time = formatTime();
    renderMessageBubble('assistant', text, time);
    messages.push({ role: 'assistant', text, timestamp: time });
    saveChatState();
    scrollToBottom();
  };

  const escapeHtml = (unsafe) => {
    return unsafe
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
  };

  // Actions
  const sendMessage = async (text) => {
    if (!text || isLoading) return;
    isLoading = true;
    
    hideEmptyState();
    errorState.classList.add('hidden');
    renderUserMessage(text);
    
    chatInput.value = '';
    setInputState(true);
    loadingIndicator.classList.remove('hidden');
    scrollToBottom();

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, conversation_id: conversationId })
      });

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();
      conversationId = data.conversation_id;
      
      loadingIndicator.classList.add('hidden');
      renderAgentMessage(data.reply);
      lastFailedMessage = null;
      
    } catch (err) {
      loadingIndicator.classList.add('hidden');
      errorDesc.textContent = "Our service experienced a temporary issue. Please try again.";
      errorState.classList.remove('hidden');
      lastFailedMessage = text;
      scrollToBottom();
    } finally {
      isLoading = false;
      setInputState(false);
      chatInput.focus();
    }
  };

  // Event Listeners
  chatInput.addEventListener('input', () => {
    sendBtn.disabled = !chatInput.value.trim() || isLoading;
  });

  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    sendMessage(chatInput.value.trim());
  });

  suggestionCards.forEach(card => {
    card.addEventListener('click', () => {
      sendMessage(card.dataset.query);
    });
  });

  retryBtn.addEventListener('click', () => {
    if (lastFailedMessage) {
      sendMessage(lastFailedMessage);
    }
  });

  clearBtn.addEventListener('click', () => {
    // Reset state
    conversationId = null;
    lastFailedMessage = null;
    isLoading = false;
    messages = [];
    clearChatState();
    setInputState(false);
    
    // Reset UI
    chatInput.value = '';
    errorState.classList.add('hidden');
    loadingIndicator.classList.add('hidden');
    emptyState.classList.remove('hidden');
    
    // Remove all dynamically added messages
    const bubbles = chatMessagesContainer.querySelectorAll('.msg-user, .msg-agent');
    bubbles.forEach(bubble => bubble.remove());
  });

  // ── Restore previous session on page load ──────────────────────
  restoreChatState();

});
