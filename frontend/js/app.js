/**
 * FloodLens AI Main Application Controller
 */
document.addEventListener('DOMContentLoaded', async () => {
  // 1. Initialize Map & Assistant UI
  const mapManager = new FloodLensMap('map');
  const assistantUI = new CitizenAssistantUI(mapManager);

  // 2. UI Element References
  const districtSelect = document.getElementById('district-select');
  const scenarioSelect = document.getElementById('scenario-select');
  const refreshBtn = document.getElementById('refresh-btn');
  const btnGeneratePlan = document.getElementById('btn-generate-plan');
  const btnApproveDispatch = document.getElementById('btn-approve-dispatch');
  const reportForm = document.getElementById('report-form');
  const depthSlider = document.getElementById('report-depth');
  const depthDisplay = document.getElementById('depth-val-display');

  // Modal elements
  const allIndiaModal = document.getElementById('all-india-modal');
  const btnAllIndiaModal = document.getElementById('btn-all-india-modal');
  const btnCloseModal = document.getElementById('btn-close-modal');
  const modalSearch = document.getElementById('modal-region-search');
  const modalGrid = document.getElementById('modal-regions-grid');
  const filterZoneBtns = document.querySelectorAll('.filter-zone-btn');
  const btnIndiaOverview = document.getElementById('btn-india-overview');

  // Tab buttons
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  // Layer toggles
  const layerRoads = document.getElementById('layer-roads');
  const layerHospitals = document.getElementById('layer-hospitals');
  const layerCommunities = document.getElementById('layer-communities');
  const layerReports = document.getElementById('layer-reports');

  let allDistricts = [];
  let activeZoneFilter = 'all';

  // 3. Tab Switching Logic
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTabId = btn.getAttribute('data-tab');

      tabBtns.forEach(b => {
        b.classList.remove('border-blue-500', 'text-blue-400');
        b.classList.add('border-transparent', 'text-slate-400');
      });
      btn.classList.add('border-blue-500', 'text-blue-400');
      btn.classList.remove('border-transparent', 'text-slate-400');

      tabContents.forEach(c => {
        if (c.id === targetTabId) {
          c.classList.remove('hidden');
        } else {
          c.classList.add('hidden');
        }
      });
    });
  });

  // 4. Map Intelligence Layers Box Open / Close Logic
  const mapLayersBox = document.getElementById('map-layers-box');
  const btnCloseMapLayers = document.getElementById('btn-close-map-layers');
  const btnOpenMapLayers = document.getElementById('btn-open-map-layers');

  function setLayersBoxOpen(isOpen) {
    if (!mapLayersBox || !btnOpenMapLayers) return;
    if (isOpen) {
      mapLayersBox.classList.remove('hidden');
      mapLayersBox.style.display = 'block';
      btnOpenMapLayers.classList.add('hidden');
      btnOpenMapLayers.style.display = 'none';
    } else {
      mapLayersBox.classList.add('hidden');
      mapLayersBox.classList.remove('block', 'md:block');
      mapLayersBox.style.display = 'none';
      btnOpenMapLayers.classList.remove('hidden', 'md:hidden');
      btnOpenMapLayers.classList.add('flex');
      btnOpenMapLayers.style.display = 'inline-flex';
    }
  }

  if (btnCloseMapLayers) {
    btnCloseMapLayers.addEventListener('click', () => setLayersBoxOpen(false));
  }
  if (btnOpenMapLayers) {
    btnOpenMapLayers.addEventListener('click', () => setLayersBoxOpen(true));
  }

  // On phone screens (< 768px), default to closed so the map is unobstructed
  if (window.innerWidth < 768) {
    setLayersBoxOpen(false);
  } else {
    setLayersBoxOpen(true);
  }

  // 5. Universal Navigation & View Switcher Logic
  const mapSection = document.getElementById('map-section');
  const sidebarSection = document.getElementById('sidebar-section');
  const mobileNavBtns = document.querySelectorAll('.mobile-nav-btn');
  const btnBackToMap = document.getElementById('btn-back-to-map');
  const btnFloatingViewHub = document.getElementById('btn-floating-view-hub');
  const hdrBtnMap = document.getElementById('hdr-btn-map');
  const hdrBtnHub = document.getElementById('hdr-btn-hub');

  const mobileSidebarTitle = document.getElementById('mobile-sidebar-title');
  const viewTitles = {
    'tab-dashboard': 'Authority Hub',
    'tab-assistant': 'Citizen Safe-Access Bot',
    'tab-report': 'Submit Ground Report',
    'tab-diagnostics': 'ML Failure Diagnostics'
  };

  function switchView(viewName) {
    const isMobile = window.innerWidth < 768;

    // Update Header Fast View Switcher Buttons
    if (hdrBtnMap && hdrBtnHub) {
      if (viewName === 'map') {
        hdrBtnMap.classList.add('bg-blue-600', 'text-white');
        hdrBtnMap.classList.remove('text-slate-400');
        hdrBtnHub.classList.remove('bg-blue-600', 'text-white');
        hdrBtnHub.classList.add('text-slate-400');
      } else {
        hdrBtnHub.classList.add('bg-blue-600', 'text-white');
        hdrBtnHub.classList.remove('text-slate-400');
        hdrBtnMap.classList.remove('bg-blue-600', 'text-white');
        hdrBtnMap.classList.add('text-slate-400');
      }
    }

    // Update Mobile Bottom Nav Pills
    mobileNavBtns.forEach(btn => {
      const bView = btn.getAttribute('data-mobile-view');
      if (bView === viewName) {
        btn.classList.add('text-blue-400');
        btn.classList.remove('text-slate-400');
      } else {
        btn.classList.remove('text-blue-400');
        btn.classList.add('text-slate-400');
      }
    });

    if (viewName === 'map') {
      if (mapSection) {
        mapSection.classList.remove('hidden');
        mapSection.classList.add('flex');
        // Scroll map into view (crucial for desktop site mode on mobile)
        mapSection.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'start' });
      }
      if (isMobile && sidebarSection) {
        sidebarSection.classList.add('hidden');
        sidebarSection.classList.remove('flex');
      }
      if (btnFloatingViewHub) {
        btnFloatingViewHub.classList.remove('hidden');
      }
      setTimeout(() => {
        if (mapManager && mapManager.map) mapManager.map.invalidateSize();
      }, 80);
    } else {
      // Switching to a Sidebar Tab (Hub, Bot, Report, ML)
      if (btnFloatingViewHub) {
        btnFloatingViewHub.classList.add('hidden');
      }

      if (isMobile && mapSection) {
        mapSection.classList.add('hidden');
        mapSection.classList.remove('flex');
      }

      if (sidebarSection) {
        sidebarSection.classList.remove('hidden');
        sidebarSection.classList.add('flex', 'w-full');
        // Scroll sidebar into view (allows seamless navigation even when zoomed in desktop site!)
        sidebarSection.scrollIntoView({ behavior: 'smooth', block: 'start', inline: 'start' });
      }

      if (mobileSidebarTitle && viewTitles[viewName]) {
        mobileSidebarTitle.textContent = viewTitles[viewName];
      }

      // Activate corresponding tab button & tab content in sidebar
      tabBtns.forEach(b => {
        const tId = b.getAttribute('data-tab');
        if (tId === viewName) {
          b.classList.add('border-blue-500', 'text-blue-400');
          b.classList.remove('border-transparent', 'text-slate-400');
        } else {
          b.classList.remove('border-blue-500', 'text-blue-400');
          b.classList.add('border-transparent', 'text-slate-400');
        }
      });

      tabContents.forEach(c => {
        if (c.id === viewName) {
          c.classList.remove('hidden');
        } else {
          c.classList.add('hidden');
        }
      });
    }
  }

  // Hook all interactive view-switching triggers
  mobileNavBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetView = btn.getAttribute('data-mobile-view');
      switchView(targetView);
    });
  });

  if (btnBackToMap) {
    btnBackToMap.addEventListener('click', () => switchView('map'));
  }
  if (btnFloatingViewHub) {
    btnFloatingViewHub.addEventListener('click', () => switchView('tab-dashboard'));
  }
  if (hdrBtnMap) {
    hdrBtnMap.addEventListener('click', () => switchView('map'));
  }
  if (hdrBtnHub) {
    hdrBtnHub.addEventListener('click', () => switchView('tab-dashboard'));
  }

  // Global helpers
  window.switchToMapView = function() {
    switchView('map');
  };
  window.switchMobileView = switchView;

  // Mobile Fast Controls: District Picker & Telemetry Toggle
  const btnMobileDistrictPicker = document.getElementById('btn-mobile-district-picker');
  const btnToggleTelemetry = document.getElementById('btn-toggle-telemetry');
  const mobileControlsDrawer = document.getElementById('mobile-controls-drawer');

  if (btnMobileDistrictPicker && allIndiaModal) {
    btnMobileDistrictPicker.addEventListener('click', () => {
      renderModalGrid(allDistricts);
      allIndiaModal.classList.remove('hidden');
    });
  }

  if (btnToggleTelemetry && mobileControlsDrawer) {
    btnToggleTelemetry.addEventListener('click', () => {
      mobileControlsDrawer.classList.toggle('hidden');
      mobileControlsDrawer.classList.toggle('flex');
      btnToggleTelemetry.classList.toggle('bg-blue-600');
      btnToggleTelemetry.classList.toggle('text-white');
    });
  }

  // Mobile Header Buttons (All India, API Key, Refresh)
  const btnAllIndiaMobile = document.getElementById('btn-all-india-modal-mobile');
  const btnApiKeyMobile = document.getElementById('btn-api-key-modal-mobile');
  const refreshBtnMobile = document.getElementById('refresh-btn-mobile');

  if (btnAllIndiaMobile && allIndiaModal) {
    btnAllIndiaMobile.addEventListener('click', () => {
      renderModalGrid(allDistricts);
      allIndiaModal.classList.remove('hidden');
    });
  }
  if (btnApiKeyMobile) {
    btnApiKeyMobile.addEventListener('click', () => {
      const apiKeyModal = document.getElementById('api-key-modal');
      if (apiKeyModal) apiKeyModal.classList.remove('hidden');
    });
  }
  if (refreshBtnMobile && refreshBtn) {
    refreshBtnMobile.addEventListener('click', () => refreshBtn.click());
  }

  // Initialize mobile view
  if (window.innerWidth < 768) {
    switchMobileView('map');
  }

  // Handle window resize between mobile and desktop gracefully
  window.addEventListener('resize', () => {
    if (window.innerWidth >= 768) {
      if (mapSection) {
        mapSection.classList.remove('hidden');
        mapSection.classList.add('flex');
      }
      if (sidebarSection) {
        sidebarSection.classList.remove('hidden', 'w-full');
        sidebarSection.classList.add('flex');
      }
      if (mapManager && mapManager.map) mapManager.map.invalidateSize();
    }
  });

  // 6. Layer & Basemap Handlers
  if (layerRoads) layerRoads.addEventListener('change', e => mapManager.toggleLayer('roads', e.target.checked));
  if (layerHospitals) layerHospitals.addEventListener('change', e => mapManager.toggleLayer('hospitals', e.target.checked));
  if (layerCommunities) layerCommunities.addEventListener('change', e => mapManager.toggleLayer('communities', e.target.checked));
  if (layerReports) layerReports.addEventListener('change', e => mapManager.toggleLayer('reports', e.target.checked));

  const basemapSelect = document.getElementById('basemap-select');
  if (basemapSelect) {
    basemapSelect.addEventListener('change', e => {
      mapManager.setBasemap(e.target.value);
    });
  }

  // 5. Depth Slider Sync
  if (depthSlider && depthDisplay) {
    depthSlider.addEventListener('input', e => {
      depthDisplay.textContent = `${e.target.value} cm`;
    });
  }

  // 6. Populate Districts in Select Dropdown
  async function initDistricts() {
    try {
      const res = await API.fetchDistricts();
      allDistricts = res.districts || [];

      // Group districts by region_zone
      const groups = {};
      allDistricts.forEach(d => {
        const zone = d.region_zone || d.state || 'General';
        if (!groups[zone]) groups[zone] = [];
        groups[zone].push(d);
      });

      // Clear & populate select
      districtSelect.innerHTML = '';
      for (const [zone, dists] of Object.entries(groups)) {
        const optgroup = document.createElement('optgroup');
        optgroup.label = `📍 ${zone}`;
        optgroup.className = 'bg-slate-900 font-bold text-slate-300';

        dists.forEach(d => {
          const opt = document.createElement('option');
          opt.value = d.id;
          opt.textContent = `${d.name} (${d.river.split('&')[0].trim()})`;
          opt.className = 'bg-slate-900 font-normal text-white';
          optgroup.appendChild(opt);
        });

        districtSelect.appendChild(optgroup);
      }

      // Default to patna
      districtSelect.value = 'patna';

      // Render Modal grid
      renderModalGrid(allDistricts);
    } catch (err) {
      console.error('Failed to load districts directory:', err);
    }
  }

  // 7. Render All-India Modal Cards
  function renderModalGrid(districts) {
    if (!modalGrid) return;

    const searchTerm = (modalSearch ? modalSearch.value.trim().toLowerCase() : '');

    const filtered = districts.filter(d => {
      const matchesSearch = !searchTerm ||
        d.name.toLowerCase().includes(searchTerm) ||
        d.state.toLowerCase().includes(searchTerm) ||
        d.river.toLowerCase().includes(searchTerm) ||
        (d.region_zone || '').toLowerCase().includes(searchTerm);

      const matchesZone = (activeZoneFilter === 'all') ||
        (activeZoneFilter === 'Himalayan' ? ((d.region_zone || '').includes('Himalayan') || d.state.includes('Pradesh') || d.state.includes('Kashmir')) :
        d.state.toLowerCase().includes(activeZoneFilter.toLowerCase()));

      return matchesSearch && matchesZone;
    });

    if (filtered.length === 0) {
      modalGrid.innerHTML = `
        <div class="col-span-full py-8 text-center text-slate-400">
          <i class="fa-solid fa-triangle-exclamation text-2xl text-amber-400 mb-2"></i>
          <p>No flood zones match your search criteria.</p>
        </div>
      `;
      return;
    }

    modalGrid.innerHTML = filtered.map(d => {
      const isSevere = (d.annual_flood_frequency || '').includes('Severe') || (d.annual_flood_frequency || '').includes('Flash');
      const badgeBorder = isSevere ? 'border-red-500/50 bg-red-950/30 text-red-300' : 'border-blue-500/40 bg-blue-950/30 text-blue-300';
      const isSelected = districtSelect.value === d.id;

      return `
        <div class="district-card p-3 rounded-xl border ${isSelected ? 'border-blue-500 bg-blue-950/40' : 'border-slate-800 bg-slate-950/60 hover:border-slate-700 hover:bg-slate-800/50'} cursor-pointer transition-all space-y-2 flex flex-col justify-between" onclick="window.selectDistrictById('${d.id}')">
          <div>
            <div class="flex items-center justify-between gap-1 mb-1">
              <span class="text-[10px] uppercase font-bold text-slate-400">${d.state}</span>
              <span class="text-[9px] px-1.5 py-0.5 rounded-full border ${badgeBorder} font-semibold">
                ${d.annual_flood_frequency || 'Flood Prone'}
              </span>
            </div>
            <div class="font-bold text-white text-sm tracking-tight">${d.name}</div>
            <div class="text-[11px] text-blue-300 flex items-center gap-1 mt-0.5">
              <i class="fa-solid fa-water text-[10px]"></i> ${d.river}
            </div>
          </div>

          <div class="pt-2 border-t border-slate-800/80 text-[10px] text-slate-400 space-y-0.5">
            <div>CWC Station: <span class="text-slate-300 font-mono">${d.cwc_gauge_station}</span></div>
            <div>Danger Mark: <span class="text-amber-400 font-bold">${d.danger_level_m}m</span></div>
          </div>
        </div>
      `;
    }).join('');
  }

  // Global helper for card clicks
  window.selectDistrictById = function(id) {
    if (districtSelect) {
      districtSelect.value = id;
    }
    if (allIndiaModal) {
      allIndiaModal.classList.add('hidden');
    }
    loadData();
  };

  // 8. Modal Event Handlers
  if (btnAllIndiaModal) {
    btnAllIndiaModal.addEventListener('click', () => {
      renderModalGrid(allDistricts);
      allIndiaModal.classList.remove('hidden');
    });
  }

  if (btnCloseModal) {
    btnCloseModal.addEventListener('click', () => {
      allIndiaModal.classList.add('hidden');
    });
  }

  if (allIndiaModal) {
    allIndiaModal.addEventListener('click', (e) => {
      if (e.target === allIndiaModal) {
        allIndiaModal.classList.add('hidden');
      }
    });
  }

  if (modalSearch) {
    modalSearch.addEventListener('input', () => {
      renderModalGrid(allDistricts);
    });
  }

  filterZoneBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterZoneBtns.forEach(b => {
        b.className = 'filter-zone-btn px-2 py-1 rounded bg-slate-800 text-slate-300 hover:bg-slate-700';
      });
      btn.className = 'filter-zone-btn px-2 py-1 rounded bg-blue-600/30 text-blue-300 border border-blue-500/40 font-bold';
      activeZoneFilter = btn.getAttribute('data-filter');
      renderModalGrid(allDistricts);
    });
  });

  if (btnIndiaOverview) {
    btnIndiaOverview.addEventListener('click', () => {
      mapManager.showAllIndiaOverview(allDistricts, window.selectDistrictById);
    });
  }

  // API Key Settings Modal Handlers
  const apiKeyModal = document.getElementById('api-key-modal');
  const btnApiKeyModal = document.getElementById('btn-api-key-modal');
  const btnCloseApiKeyModal = document.getElementById('btn-close-api-key-modal');
  const btnSaveApiKey = document.getElementById('btn-save-api-key');
  const btnClearApiKey = document.getElementById('btn-clear-api-key');
  const inputApiKey = document.getElementById('input-api-key');
  const apiKeyEngine = document.getElementById('api-key-active-engine');
  const apiKeyMaskedVal = document.getElementById('api-key-masked-val');

  async function refreshApiKeyStatus() {
    try {
      const status = await API.getApiKeyStatus();
      if (apiKeyEngine) apiKeyEngine.textContent = status.engine;
      if (apiKeyMaskedVal) apiKeyMaskedVal.textContent = status.masked_key || 'None (Using heuristic fallback)';
    } catch (e) {}
  }

  if (btnApiKeyModal) {
    btnApiKeyModal.addEventListener('click', async () => {
      await refreshApiKeyStatus();
      if (apiKeyModal) apiKeyModal.classList.remove('hidden');
    });
  }

  if (btnCloseApiKeyModal) {
    btnCloseApiKeyModal.addEventListener('click', () => {
      if (apiKeyModal) apiKeyModal.classList.add('hidden');
    });
  }

  if (apiKeyModal) {
    apiKeyModal.addEventListener('click', (e) => {
      if (e.target === apiKeyModal) apiKeyModal.classList.add('hidden');
    });
  }

  if (btnSaveApiKey) {
    btnSaveApiKey.addEventListener('click', async () => {
      const key = inputApiKey.value.trim();
      try {
        const res = await API.saveApiKey(key);
        alert(res.message);
        inputApiKey.value = '';
        await refreshApiKeyStatus();
        if (apiKeyModal) apiKeyModal.classList.add('hidden');
      } catch (err) {
        alert(`Error: ${err.message}`);
      }
    });
  }

  if (btnClearApiKey) {
    btnClearApiKey.addEventListener('click', async () => {
      try {
        await API.saveApiKey('');
        inputApiKey.value = '';
        await refreshApiKeyStatus();
        alert('API key cleared. System reverted to built-in heuristic NLP.');
      } catch (err) {
        alert(`Error: ${err.message}`);
      }
    });
  }

  // 9. Load & Refresh Intelligence Pipeline
  async function loadData() {
    const district = districtSelect.value || 'patna';
    const scenario = scenarioSelect.value || 'live';

    if (refreshBtn) refreshBtn.innerHTML = '<i class="fa-solid fa-arrows-rotate fa-spin text-xs"></i>';

    try {
      const data = await API.fetchFloodIntelligence(district, scenario);
      
      // Update mobile district name button
      if (data && data.district) {
        const mobDistName = document.getElementById('mobile-district-name');
        if (mobDistName) {
          const shortName = (data.district.name || '').split(',')[0].replace(/\(.*\)/, '').trim();
          mobDistName.textContent = shortName;
        }
      }

      // Update GIS map
      mapManager.renderData(data);

      // Update Dashboard
      dashboardManager.updateDashboard(data);

      // Reset any old route highlights
      mapManager.showRoutePath([]);

      // Auto generate initial dispatch plan preview
      generatePlan(false);
    } catch (err) {
      console.error('Failed to load data:', err);
      alert('Could not connect to FloodLens backend. Please check server status.');
    } finally {
      if (refreshBtn) refreshBtn.innerHTML = '<i class="fa-solid fa-arrows-rotate text-xs"></i>';
    }
  }

  // 10. Event Listeners for Filters
  districtSelect.addEventListener('change', loadData);
  scenarioSelect.addEventListener('change', loadData);
  if (refreshBtn) refreshBtn.addEventListener('click', loadData);

  // 11. Generate Dispatch Plan
  async function generatePlan(alertFeedback = true) {
    const district = districtSelect.value || 'patna';
    const scenario = scenarioSelect.value || 'live';

    try {
      const res = await API.generateDispatch(district, scenario);
      if (res.status === 'success' && res.dispatch_plan) {
        dashboardManager.renderDispatchPlan(res.dispatch_plan);
        if (alertFeedback) {
          const dashBtn = document.querySelector('[data-tab="tab-dashboard"]');
          if (dashBtn) dashBtn.click();
        }
      }
    } catch (err) {
      console.error('Plan generation failed:', err);
    }
  }

  if (btnGeneratePlan) {
    btnGeneratePlan.addEventListener('click', () => generatePlan(true));
  }

  // 12. Human Approval Flow
  if (btnApproveDispatch) {
    btnApproveDispatch.addEventListener('click', async () => {
      if (!dashboardManager.currentPlanId) return;

      const officialName = prompt('Enter Authority Sign-Off Name:', 'District Magistrate, IAS');
      if (!officialName) return;

      try {
        const res = await API.approveDispatch(dashboardManager.currentPlanId, officialName);
        if (res.status === 'success' && res.plan) {
          dashboardManager.renderDispatchPlan(res.plan);
          alert(`Dispatch Plan ${res.plan.plan_id} officially authorized and dispatched to NDRF/SDRF command!`);
        }
      } catch (err) {
        alert(`Approval error: ${err.message}`);
      }
    });
  }

  // 13. Community Report Submission
  if (reportForm) {
    reportForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const author = document.getElementById('report-author').value;
      const text = document.getElementById('report-text').value;
      const photo = document.getElementById('report-photo').value;
      const depth = parseInt(depthSlider.value, 10);
      const district = districtSelect.value;

      const submitBtn = reportForm.querySelector('button[type="submit"]');
      const originalText = submitBtn.innerHTML;
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Verifying with Gemini...';

      try {
        const payload = {
          district: district,
          author: author,
          reported_text: text,
          photo_url: photo || null
        };

        const res = await API.submitReport(payload);
        if (res.status === 'success') {
          alert(`Report verified and registered!\n• Status: ${res.report.status.toUpperCase()}\n• Language: ${res.report.language}\n• Confidence: ${Math.round(res.report.confidence * 100)}%`);
          reportForm.reset();
          if (depthSlider && depthDisplay) {
            depthSlider.value = 45;
            depthDisplay.textContent = '45 cm';
          }
          loadData();
        }
      } catch (err) {
        alert(`Error submitting report: ${err.message}`);
      } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
      }
    });
  }

  // Initialize districts and initial load
  await initDistricts();
  await loadData();
});
