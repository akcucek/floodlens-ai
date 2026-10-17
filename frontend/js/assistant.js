/**
 * FloodLens Citizen Assistant Chat Handler
 */
class CitizenAssistantUI {
  constructor(mapInstance) {
    this.map = mapInstance;
    this.chatContainer = document.getElementById('chat-messages');
    this.chatForm = document.getElementById('chat-form');
    this.chatInput = document.getElementById('chat-input');
    this.districtSelect = document.getElementById('district-select');
    this.scenarioSelect = document.getElementById('scenario-select');

    this.init();
  }

  init() {
    if (this.chatForm) {
      this.chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = this.chatInput.value.trim();
        if (text) {
          this.sendMessage(text);
          this.chatInput.value = '';
        }
      });
    }

    // Quick prompt buttons
    document.querySelectorAll('.quick-prompt').forEach(btn => {
      btn.addEventListener('click', () => {
        const text = btn.textContent.trim();
        this.sendMessage(text);
      });
    });
  }

  async sendMessage(queryText) {
    this.appendMessage('user', queryText);

    // Typing indicator
    const typingId = this.appendTypingIndicator();

    try {
      const district = this.districtSelect ? this.districtSelect.value : 'patna';
      const scenario = this.scenarioSelect ? this.scenarioSelect.value : 'live';

      const res = await API.sendChatMessage(district, queryText, scenario);
      this.removeTypingIndicator(typingId);

      this.appendMessage('assistant', res.response, res.disclaimer);

      if (res.suggested_path && res.suggested_path.length > 0) {
        this.map.showRoutePath(res.suggested_path);
      }
    } catch (err) {
      this.removeTypingIndicator(typingId);
      this.appendMessage('assistant', `⚠️ Sorry, could not process request: ${err.message}`);
    }
  }

  appendMessage(role, text, disclaimer = null) {
    if (!this.chatContainer) return;

    const msgDiv = document.createElement('div');
    msgDiv.className = 'flex items-start gap-2.5';

    if (role === 'user') {
      msgDiv.className = 'flex items-start gap-2.5 justify-end';
      msgDiv.innerHTML = `
        <div class="bg-blue-600 text-white rounded-lg p-2.5 max-w-[85%] text-xs shadow-md">
          ${this.escapeHtml(text)}
        </div>
        <div class="w-7 h-7 rounded-full bg-slate-700 flex items-center justify-center shrink-0 text-white font-bold text-xs">
          <i class="fa-solid fa-user text-[10px]"></i>
        </div>
      `;
    } else {
      // Format markdown-like bold and bullet lines
      const formatted = this.formatMarkdown(text);
      msgDiv.innerHTML = `
        <div class="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center shrink-0 text-white font-bold text-xs">
          FL
        </div>
        <div class="bg-slate-800 rounded-lg p-2.5 max-w-[85%] text-slate-200 text-xs shadow-md space-y-1.5">
          <div>${formatted}</div>
          ${disclaimer ? `
            <div class="text-[10px] text-amber-300 bg-amber-950/40 border border-amber-500/30 p-1.5 rounded mt-1.5">
              ${disclaimer}
            </div>
          ` : ''}
        </div>
      `;
    }

    this.chatContainer.appendChild(msgDiv);
    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
  }

  appendTypingIndicator() {
    if (!this.chatContainer) return null;
    const id = 'typing-' + Date.now();
    const div = document.createElement('div');
    div.id = id;
    div.className = 'flex items-start gap-2.5';
    div.innerHTML = `
      <div class="w-7 h-7 rounded-full bg-blue-600 flex items-center justify-center shrink-0 text-white font-bold text-xs">
        FL
      </div>
      <div class="bg-slate-800 rounded-lg p-2.5 text-xs text-slate-400 flex items-center gap-1.5">
        <span class="w-1.5 h-1.5 rounded-full bg-slate-400 animate-ping"></span>
        <span>Analyzing hydrological models & shortest paths...</span>
      </div>
    `;
    this.chatContainer.appendChild(div);
    this.chatContainer.scrollTop = this.chatContainer.scrollHeight;
    return id;
  }

  removeTypingIndicator(id) {
    if (!id) return;
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }

  formatMarkdown(text) {
    let out = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/\n\n/g, '<br><br>')
      .replace(/\n• /g, '<br>• ');
    return out;
  }
}
