/**
 * FloodLens AI Client API Interface
 */
const API = {
  baseUrl: window.location.origin,

  async fetchDistricts() {
    const res = await fetch(`${this.baseUrl}/api/districts`);
    if (!res.ok) throw new Error("Failed to load districts");
    return await res.json();
  },

  async fetchFloodIntelligence(district = "patna", scenario = "live") {
    const res = await fetch(`${this.baseUrl}/api/flood-intelligence?district=${encodeURIComponent(district)}&scenario=${encodeURIComponent(scenario)}`);
    if (!res.ok) throw new Error("Failed to load flood intelligence");
    return await res.json();
  },

  async submitReport(data) {
    const res = await fetch(`${this.baseUrl}/api/reports/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error("Failed to submit report");
    return await res.json();
  },

  async generateDispatch(district = "patna", scenario = "live") {
    const res = await fetch(`${this.baseUrl}/api/agent/generate-dispatch?district=${encodeURIComponent(district)}&scenario=${encodeURIComponent(scenario)}`, {
      method: "POST"
    });
    if (!res.ok) throw new Error("Failed to generate dispatch plan");
    return await res.json();
  },

  async approveDispatch(planId, officialName) {
    const res = await fetch(`${this.baseUrl}/api/agent/approve-dispatch`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ plan_id: planId, official_name: officialName })
    });
    if (!res.ok) throw new Error("Failed to approve dispatch");
    return await res.json();
  },

  async sendChatMessage(district, query, scenario = "live") {
    const res = await fetch(`${this.baseUrl}/api/assistant/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ district, query, scenario })
    });
    if (!res.ok) throw new Error("Failed to chat with assistant");
    return await res.json();
  },

  async getApiKeyStatus() {
    const res = await fetch(`${this.baseUrl}/api/settings/api-key`);
    if (!res.ok) throw new Error("Failed to get API key status");
    return await res.json();
  },

  async saveApiKey(apiKey) {
    const res = await fetch(`${this.baseUrl}/api/settings/api-key`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ api_key: apiKey })
    });
    if (!res.ok) throw new Error("Failed to save API key");
    return await res.json();
  }
};
