/**
 * FloodLens Dashboard Manager
 */
class DashboardManager {
  constructor() {
    this.currentData = null;
    this.currentPlanId = null;
  }

  updateDashboard(data) {
    this.currentData = data;
    this.updateTelemetry(data);
    this.updateAlerts(data.alerts || []);
    this.updateKPIs(data);
    this.updateCommunitiesList(data.isolation_analysis?.communities || []);
    this.updateDiagnosticsTable(data.road_predictions || []);
    this.updateReportsFeed(data.community_reports || []);
  }

  updateTelemetry(data) {
    const weather = data.weather || {};
    const river = data.river_discharge || {};
    const gauge = data.gauge || {};

    // Rain
    const rainEl = document.getElementById('telemetry-rain');
    if (rainEl) {
      rainEl.innerHTML = `${weather.rain_next_24h_mm || 0} <span class="font-normal text-slate-400">mm</span>`;
    }

    // River Discharge
    const disEl = document.getElementById('telemetry-discharge');
    if (disEl) {
      disEl.innerHTML = `${river.current_discharge_m3s || 0} <span class="font-normal text-slate-400">m³/s</span>`;
    }

    // Gauge vs Danger
    const gaugeEl = document.getElementById('telemetry-gauge');
    const gaugeCard = document.getElementById('telemetry-gauge-card');
    const gaugeIcon = document.getElementById('gauge-icon');

    if (gaugeEl) {
      const cur = gauge.current_gauge_m || 0;
      const danger = gauge.danger_level_m || 0;
      gaugeEl.innerHTML = `${cur}m <span class="text-[10px] text-slate-400">/ ${danger}m</span>`;

      if (gauge.above_danger) {
        gaugeEl.className = 'font-bold text-red-400 animate-pulse';
        if (gaugeIcon) gaugeIcon.className = 'fa-solid fa-triangle-exclamation text-red-500 animate-bounce';
        if (gaugeCard) gaugeCard.className = 'bg-red-950/40 border border-red-500/60 rounded-md px-3 py-1 flex items-center gap-2';
      } else if (gauge.above_warning) {
        gaugeEl.className = 'font-bold text-amber-400';
        if (gaugeIcon) gaugeIcon.className = 'fa-solid fa-triangle-exclamation text-amber-400';
        if (gaugeCard) gaugeCard.className = 'bg-amber-950/40 border border-amber-500/60 rounded-md px-3 py-1 flex items-center gap-2';
      } else {
        gaugeEl.className = 'font-bold text-emerald-400';
        if (gaugeIcon) gaugeIcon.className = 'fa-solid fa-shield-check text-emerald-400';
        if (gaugeCard) gaugeCard.className = 'bg-slate-800/80 border border-slate-700/60 rounded-md px-3 py-1 flex items-center gap-2';
      }
    }
  }

  updateAlerts(alerts) {
    const container = document.getElementById('active-alert-container');
    if (!container) return;

    if (!alerts || alerts.length === 0) {
      container.innerHTML = `
        <div class="p-3 rounded-xl bg-emerald-950/30 border border-emerald-500/40 text-emerald-300 text-xs flex items-center justify-between shadow-sm">
          <div class="flex items-center gap-2.5">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
            <div>
              <div class="font-bold text-emerald-200">NO ACTIVE WEATHER WARNINGS</div>
              <p class="text-[11px] text-emerald-300/80 mt-0.5">Real-time precipitation & river gauges are within safe baseline limits (IMD & CWC Normal).</p>
            </div>
          </div>
          <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
            GREEN
          </span>
        </div>
      `;
      return;
    }

    container.innerHTML = alerts.map(a => {
      const isRed = a.level === 'RED';
      const isOrange = a.level === 'ORANGE';
      const border = isRed ? 'border-red-500/60 bg-red-950/40' : (isOrange ? 'border-amber-500/60 bg-amber-950/40' : 'border-blue-500/40 bg-blue-950/30');
      const badge = isRed ? 'bg-red-500/20 text-red-300 border-red-500/40' : (isOrange ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' : 'bg-blue-500/20 text-blue-300 border-blue-500/40');

      return `
        <div class="p-3 rounded-xl border ${border} text-xs shadow-md space-y-1.5">
          <div class="flex items-center justify-between">
            <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase border ${badge}">
              ${a.level} ALERT • ${a.agency}
            </span>
            <span class="text-[10px] text-slate-400">${a.expires}</span>
          </div>
          <div class="font-bold text-white text-[13px]">${a.headline}</div>
          <div class="text-slate-300 text-[11px] leading-relaxed">${a.description}</div>
          <div class="text-[11px] font-semibold text-amber-300 pt-1 border-t border-slate-800">
            <i class="fa-solid fa-person-shelter mr-1"></i> Action: ${a.recommended_action}
          </div>
        </div>
      `;
    }).join('');
  }

  updateKPIs(data) {
    const iso = data.isolation_analysis || {};
    const summary = iso.summary || {};
    const predictions = data.road_predictions || [];

    const failedRoads = predictions.filter(p => p.status === 'impassable').length;
    const totalComms = summary.total_communities || 1;
    const safeComms = summary.safe_count || 0;
    const reachability = Math.round((safeComms / totalComms) * 100);

    const kpiIso = document.getElementById('kpi-isolated-count');
    const kpiPop = document.getElementById('kpi-population-cutoff');
    const kpiFailed = document.getElementById('kpi-failed-roads');
    const kpiHosp = document.getElementById('kpi-hospital-status');

    if (kpiIso) kpiIso.textContent = summary.isolated_count || 0;
    if (kpiPop) kpiPop.textContent = (summary.population_cut_off || 0).toLocaleString();
    if (kpiFailed) kpiFailed.textContent = failedRoads;
    if (kpiHosp) {
      kpiHosp.textContent = `${reachability}%`;
      kpiHosp.className = reachability > 70 ? 'text-xl font-extrabold text-emerald-400' : (reachability > 40 ? 'text-xl font-extrabold text-amber-400' : 'text-xl font-extrabold text-red-400');
    }
  }

  updateCommunitiesList(communities) {
    const list = document.getElementById('communities-status-list');
    if (!list) return;

    list.innerHTML = communities.map(c => {
      const isIso = c.status === 'ISOLATED';
      const isDetour = c.status === 'DETOUR_REQUIRED';
      const badgeClass = isIso ? 'badge-critical' : (isDetour ? 'badge-warning' : 'badge-safe');
      const icon = isIso ? 'fa-triangle-exclamation text-red-400' : (isDetour ? 'fa-route text-amber-400' : 'fa-circle-check text-emerald-400');

      return `
        <div class="bg-slate-900/80 border border-slate-800 p-2.5 rounded-lg flex items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <i class="fa-solid ${icon} text-sm"></i>
            <div>
              <div class="font-bold text-white">${c.name}</div>
              <div class="text-[10px] text-slate-400">Pop: ${c.population.toLocaleString()} (Vulnerable: ${c.vulnerable_population.toLocaleString()})</div>
            </div>
          </div>
          <span class="px-2 py-0.5 rounded text-[10px] font-bold ${badgeClass}">
            ${c.status}
          </span>
        </div>
      `;
    }).join('');
  }

  updateDiagnosticsTable(predictions) {
    const tbody = document.getElementById('diagnostics-table-body');
    if (!tbody) return;

    tbody.innerHTML = predictions.slice(0, 7).map(p => {
      const probColor = p.status_color || '#10b981';
      return `
        <tr class="hover:bg-slate-800/50">
          <td class="p-2 text-white font-sans font-medium">${p.segment_name}</td>
          <td class="p-2 uppercase font-semibold ${p.baseline_threshold_prediction === 'impassable' ? 'text-red-400' : 'text-emerald-400'}">
            ${p.baseline_threshold_prediction}
          </td>
          <td class="p-2 font-bold" style="color:${probColor}">
            ${(p.probability_impassable * 100).toFixed(0)}% (${p.status})
          </td>
          <td class="p-2 text-slate-400">
            [${(p.quantile_10 * 100).toFixed(0)}% - ${(p.quantile_90 * 100).toFixed(0)}%]
          </td>
        </tr>
      `;
    }).join('');
  }

  updateReportsFeed(reports) {
    const feed = document.getElementById('reports-feed');
    if (!feed) return;

    feed.innerHTML = reports.map(r => `
      <div class="bg-slate-900/90 border border-slate-800 p-3 rounded-xl space-y-1.5">
        <div class="flex items-center justify-between">
          <span class="font-bold text-white text-xs">${r.author}</span>
          <span class="text-[10px] bg-purple-500/20 text-purple-300 border border-purple-500/30 px-1.5 py-0.5 rounded font-bold uppercase">
            ${r.status}
          </span>
        </div>
        <div class="text-slate-300 italic text-xs">"${r.reported_text}"</div>
        ${r.english_summary ? `<div class="text-[11px] text-slate-400"><strong>Translation/Summary:</strong> ${r.english_summary}</div>` : ''}
        <div class="flex items-center justify-between text-[10px] text-slate-500 pt-1 border-t border-slate-800">
          <span>Depth: <strong class="text-white">${r.water_depth_cm}cm</strong> • Conf: <strong class="text-emerald-400">${Math.round(r.confidence * 100)}%</strong></span>
          <span>${r.timestamp}</span>
        </div>
      </div>
    `).join('');
  }

  renderDispatchPlan(plan) {
    this.currentPlanId = plan.plan_id;
    const summaryEl = document.getElementById('plan-evidence-summary');
    if (summaryEl) summaryEl.textContent = plan.evidence_summary;

    const badgeEl = document.getElementById('approval-status-badge');
    const approveBtn = document.getElementById('btn-approve-dispatch');

    if (badgeEl) {
      badgeEl.textContent = plan.approval_state;
      badgeEl.className = plan.approval_state.includes('APPROVED') ? 'text-xs font-bold text-emerald-400' : 'text-xs font-bold text-amber-400';
    }

    if (approveBtn) {
      if (plan.approval_state.includes('APPROVED')) {
        approveBtn.disabled = true;
        approveBtn.innerHTML = `<i class="fa-solid fa-check-double mr-1"></i> Dispatched & Signed (${plan.approved_by || 'Authority'})`;
        approveBtn.className = 'bg-slate-700 text-slate-400 text-xs px-3 py-1.5 rounded-md font-semibold cursor-not-allowed';
      } else {
        approveBtn.disabled = false;
        approveBtn.innerHTML = `<i class="fa-solid fa-signature"></i> Sign & Approve Dispatch`;
        approveBtn.className = 'bg-emerald-600 hover:bg-emerald-500 text-white text-xs px-3 py-1.5 rounded-md font-semibold transition-colors flex items-center gap-1.5';
      }
    }

    const list = document.getElementById('dispatch-priorities-list');
    if (!list) return;

    list.innerHTML = (plan.priorities || []).map(p => `
      <div class="bg-slate-900/90 border border-slate-700/80 p-2.5 rounded-lg space-y-1">
        <div class="flex items-center justify-between">
          <div class="font-bold text-white text-xs flex items-center gap-1.5">
            <span class="w-4 h-4 rounded-full bg-blue-600 text-white flex items-center justify-center text-[10px] font-bold">#${p.rank}</span>
            <span>${p.target_area}</span>
          </div>
          <span class="text-[10px] font-bold ${p.urgency.includes('P1') ? 'text-red-400' : (p.urgency.includes('P2') ? 'text-amber-400' : 'text-emerald-400')}">
            ${p.urgency}
          </span>
        </div>
        <div class="text-[11px] text-slate-300 leading-snug">
          <strong>Action:</strong> ${p.recommended_action}
        </div>
        <div class="text-[10px] text-blue-300 bg-blue-950/40 p-1 rounded">
          <strong>Resources:</strong> ${p.resource_package} • <em>${p.assigned_unit}</em>
        </div>
      </div>
    `).join('');
  }
}

const dashboardManager = new DashboardManager();
