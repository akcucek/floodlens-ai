/**
 * FloodLens GIS Map Manager
 */
class FloodLensMap {
  constructor(containerId) {
    this.map = L.map(containerId, {
      zoomControl: false,
      attributionControl: true
    }).setView([25.5941, 85.1376], 12);

    L.control.zoom({ position: 'bottomright' }).addTo(this.map);

    // Free keyless tactical base tile layer (ESRI World Dark Canvas)
    this.baseLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}', {
      attribution: '&copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
      maxZoom: 16
    }).addTo(this.map);

    this.labelsLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 16
    }).addTo(this.map);

    this.satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      attribution: '&copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
      maxZoom: 18
    });

    this.topoLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
      attribution: '&copy; Esri &mdash; Sources: GEBCO, NOAA, CHS, OSU, UNH, CSUMB, National Geographic, DeLorme, NAVTEQ, and Esri',
      maxZoom: 18
    });

    // Layer groups
    this.roadsLayer = L.layerGroup().addTo(this.map);
    this.hospitalsLayer = L.layerGroup().addTo(this.map);
    this.communitiesLayer = L.layerGroup().addTo(this.map);
    this.reportsLayer = L.layerGroup().addTo(this.map);
    this.routeLayer = L.layerGroup().addTo(this.map);
    this.allIndiaLayer = L.layerGroup().addTo(this.map);

    this.activeData = null;
  }

  setBasemap(type) {
    if (this.map.hasLayer(this.baseLayer)) this.map.removeLayer(this.baseLayer);
    if (this.map.hasLayer(this.labelsLayer)) this.map.removeLayer(this.labelsLayer);
    if (this.map.hasLayer(this.satelliteLayer)) this.map.removeLayer(this.satelliteLayer);
    if (this.map.hasLayer(this.topoLayer)) this.map.removeLayer(this.topoLayer);

    if (type === 'satellite') {
      this.satelliteLayer.addTo(this.map);
    } else if (type === 'topo') {
      this.topoLayer.addTo(this.map);
    } else {
      this.baseLayer.addTo(this.map);
      this.labelsLayer.addTo(this.map);
    }
  }

  setCenter(center, zoom = 12) {
    this.map.setView(center, zoom);
  }

  renderData(data) {
    this.activeData = data;
    this.clearLayers();

    // 1. Center map if needed
    if (data.district && data.district.center) {
      this.map.setView(data.district.center, data.district.zoom || 12);
    }

    // 2. Render Road Network
    this.renderRoads(data);

    // 3. Render Hospitals
    this.renderHospitals(data.hospitals || []);

    // 4. Render Communities & Isolation Zones
    this.renderCommunities(data.isolation_analysis?.communities || []);

    // 5. Render Verified Reports
    this.renderReports(data.community_reports || []);
  }

  clearLayers() {
    this.roadsLayer.clearLayers();
    this.hospitalsLayer.clearLayers();
    this.communitiesLayer.clearLayers();
    this.reportsLayer.clearLayers();
    this.routeLayer.clearLayers();
    this.allIndiaLayer.clearLayers();
  }

  renderRoads(data) {
    const nodes = data.nodes || {};
    const predictions = data.road_predictions || [];
    const predMap = {};
    predictions.forEach(p => predMap[p.segment_id] = p);

    (data.road_segments || []).forEach(seg => {
      const uNode = nodes[seg.u];
      const vNode = nodes[seg.v];
      if (!uNode || !vNode) return;

      const pred = predMap[seg.id] || {
        probability_impassable: 0.1,
        status: 'passable',
        status_color: '#10b981',
        estimated_water_depth_cm: 0
      };

      const polyline = L.polyline(
        [[uNode.lat, uNode.lon], [vNode.lat, vNode.lon]],
        {
          color: pred.status_color,
          weight: pred.status === 'impassable' ? 5 : 4,
          opacity: 0.85,
          dashArray: pred.status === 'impassable' ? '6, 6' : null
        }
      );

      // Popup with intelligence diagnostics
      const popupContent = `
        <div class="p-1 space-y-1.5 text-xs">
          <div class="font-bold text-sm text-white flex items-center justify-between border-b border-slate-700 pb-1">
            <span>${seg.name}</span>
            <span class="px-1.5 py-0.5 rounded text-[10px] font-semibold uppercase" style="background:${pred.status_color}33; color:${pred.status_color};">
              ${pred.status}
            </span>
          </div>
          <div class="grid grid-cols-2 gap-1 text-[11px] text-slate-300">
            <div>Class: <span class="text-white font-mono">${seg.road_class}</span></div>
            <div>Elevation: <span class="text-white font-mono">${seg.elevation_m}m</span></div>
            <div>Impassable Prob: <span class="font-mono font-bold" style="color:${pred.status_color}">${(pred.probability_impassable * 100).toFixed(1)}%</span></div>
            <div>Est. Water Depth: <span class="text-white font-mono">${pred.estimated_water_depth_cm} cm</span></div>
          </div>
          <div class="text-[11px] bg-slate-800/80 p-1.5 rounded text-slate-300">
            <span class="text-slate-400 font-semibold">Key Risk Drivers:</span><br>
            ${(pred.key_drivers || []).map(d => `• ${d}`).join('<br>')}
          </div>
          <div class="text-[10px] text-emerald-400 border-t border-slate-800 pt-1">
            <i class="fa-solid fa-microchip"></i> <strong>ML Advantage:</strong> ${pred.model_advantage_note || 'Enhanced multi-factor prediction.'}
          </div>
        </div>
      `;

      polyline.bindPopup(popupContent);
      this.roadsLayer.addLayer(polyline);
    });
  }

  renderHospitals(hospitals) {
    hospitals.forEach(h => {
      const icon = L.divIcon({
        className: 'custom-hosp-marker',
        html: `
          <div class="w-7 h-7 rounded-lg bg-blue-600 border-2 border-white shadow-lg flex items-center justify-center text-white text-xs cursor-pointer hover:scale-110 transition-transform">
            <i class="fa-solid fa-hospital"></i>
          </div>
        `,
        iconSize: [28, 28],
        iconAnchor: [14, 14]
      });

      const marker = L.marker([h.lat, h.lon], { icon });
      marker.bindPopup(`
        <div class="p-1 space-y-1 text-xs">
          <div class="font-bold text-sm text-blue-400 border-b border-slate-700 pb-1 flex items-center justify-between">
            <span>${h.name}</span>
            <span class="text-[10px] bg-blue-500/20 text-blue-300 px-1.5 py-0.5 rounded">OPEN</span>
          </div>
          <div class="text-slate-300 text-[11px]">Type: <span class="text-white">${h.type.replace('_', ' ').toUpperCase()}</span></div>
          <div class="text-slate-300 text-[11px]">Bed Capacity: <span class="text-emerald-400 font-bold">${h.beds} beds</span></div>
          <div class="text-slate-300 text-[11px]">ICU Equipment: <span class="text-white">${h.icu_available ? 'Available' : 'Unavailable'}</span></div>
          <div class="text-slate-300 text-[11px]">Generator Backup: <span class="text-white">${h.backup_generator ? 'Yes' : 'No'}</span></div>
        </div>
      `);
      this.hospitalsLayer.addLayer(marker);
    });
  }

  renderCommunities(communities) {
    communities.forEach(c => {
      const isIsolated = c.status === 'ISOLATED';
      const isDetour = c.status === 'DETOUR_REQUIRED';

      const color = isIsolated ? '#ef4444' : (isDetour ? '#f59e0b' : '#10b981');
      const pulseClass = isIsolated ? 'pulsing-isolated-marker' : '';

      const icon = L.divIcon({
        className: 'custom-comm-marker',
        html: `
          <div class="w-6 h-6 rounded-full border-2 border-slate-900 flex items-center justify-center text-white text-[10px] ${pulseClass}" style="background:${color};">
            <i class="fa-solid ${isIsolated ? 'fa-triangle-exclamation' : 'fa-users'}"></i>
          </div>
        `,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });

      const marker = L.marker([c.lat, c.lon], { icon });
      
      const acc = c.access_details || {};
      const markerPopup = `
        <div class="p-1 space-y-1.5 text-xs">
          <div class="font-bold text-sm text-white border-b border-slate-700 pb-1 flex items-center justify-between">
            <span>${c.name}</span>
            <span class="px-1.5 py-0.5 rounded text-[10px] font-bold" style="background:${color}33; color:${color};">
              ${c.status}
            </span>
          </div>
          <div class="text-slate-300 text-[11px]">Population: <span class="text-white font-semibold">${c.population.toLocaleString()}</span> (Vulnerable: <span class="text-amber-400">${c.vulnerable_population.toLocaleString()}</span>)</div>
          <div class="text-slate-300 text-[11px]">Status: <span class="font-semibold text-white">${acc.reason || 'Normal connectivity'}</span></div>
          ${acc.reachable && acc.target_hospital ? `
            <div class="bg-slate-800/80 p-1.5 rounded text-[11px]">
              <span class="text-slate-400">Target Facility:</span> <strong class="text-blue-300">${acc.target_hospital.name}</strong><br>
              <span class="text-slate-400">Distance:</span> ${acc.distance_km} km (~${acc.est_time_mins} mins)
            </div>
          ` : `
            <div class="bg-red-950/60 border border-red-500/40 p-1.5 rounded text-[11px] text-red-200">
              🚨 <strong>ALL ACCESS ROUTES CUT OFF</strong>. Watercraft rescue / air-drop required.
            </div>
          `}
        </div>
      `;

      marker.bindPopup(markerPopup);
      this.communitiesLayer.addLayer(marker);
    });
  }

  renderReports(reports) {
    reports.forEach(r => {
      const icon = L.divIcon({
        className: 'custom-report-marker',
        html: `
          <div class="w-6 h-6 rounded-md bg-purple-600 border border-purple-300 shadow flex items-center justify-center text-white text-[10px] cursor-pointer hover:scale-110 transition-transform">
            <i class="fa-solid fa-camera"></i>
          </div>
        `,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });

      const marker = L.marker([r.lat, r.lon], { icon });
      marker.bindPopup(`
        <div class="p-1 space-y-1.5 text-xs max-w-[240px]">
          <div class="font-bold text-purple-300 border-b border-slate-700 pb-1 flex items-center justify-between">
            <span>Verified Citizen Report</span>
            <span class="text-[10px] bg-purple-500/20 text-purple-200 px-1 py-0.5 rounded">${r.status.toUpperCase()}</span>
          </div>
          <div class="text-slate-300 italic">"${r.reported_text}"</div>
          ${r.english_summary ? `<div class="text-[11px] text-slate-400"><strong>Summary:</strong> ${r.english_summary}</div>` : ''}
          <div class="grid grid-cols-2 gap-1 text-[11px] text-slate-300 bg-slate-800 p-1 rounded">
            <div>Water Depth: <span class="text-white font-bold">${r.water_depth_cm} cm</span></div>
            <div>Confidence: <span class="text-emerald-400 font-bold">${Math.round(r.confidence * 100)}%</span></div>
          </div>
          ${r.photo_url ? `<img src="${r.photo_url}" alt="Report Photo" class="w-full h-24 object-cover rounded mt-1 border border-slate-700">` : ''}
          <div class="text-[10px] text-slate-500">Source: ${r.source} (${r.timestamp})</div>
        </div>
      `);
      this.reportsLayer.addLayer(marker);
    });
  }

  showRoutePath(pathSegments) {
    this.routeLayer.clearLayers();
    if (!pathSegments || pathSegments.length === 0 || !this.activeData) return;

    const nodes = this.activeData.nodes || {};
    const coords = [];

    pathSegments.forEach(seg => {
      const uNode = nodes[seg.u];
      const vNode = nodes[seg.v];
      if (uNode && vNode) {
        coords.push([uNode.lat, uNode.lon]);
        coords.push([vNode.lat, vNode.lon]);
      }
    });

    if (coords.length > 0) {
      const routeLine = L.polyline(coords, {
        color: '#06b6d4', // cyan-500
        weight: 6,
        opacity: 0.9,
        lineCap: 'round'
      });
      this.routeLayer.addLayer(routeLine);
      this.map.fitBounds(routeLine.getBounds(), { padding: [50, 50] });
    }
  }

  toggleLayer(layerName, visible) {
    const layerMap = {
      roads: this.roadsLayer,
      hospitals: this.hospitalsLayer,
      communities: this.communitiesLayer,
      reports: this.reportsLayer
    };

    const target = layerMap[layerName];
    if (target) {
      if (visible && !this.map.hasLayer(target)) {
        this.map.addLayer(target);
      } else if (!visible && this.map.hasLayer(target)) {
        this.map.removeLayer(target);
      }
    }
  }

  showAllIndiaOverview(districts, onSelectDistrict) {
    this.clearLayers();
    // Center overview on India
    this.map.setView([22.5937, 80.9629], 5);

    districts.forEach(d => {
      const isSevere = (d.annual_flood_frequency || '').includes('Severe') || (d.annual_flood_frequency || '').includes('Flash');
      const pinColor = isSevere ? '#ef4444' : '#3b82f6';

      const icon = L.divIcon({
        className: 'custom-india-pin',
        html: `
          <div class="relative cursor-pointer hover:scale-125 transition-transform">
            <div class="w-6 h-6 rounded-full border-2 border-white shadow-xl flex items-center justify-center text-white text-[10px] font-bold" style="background:${pinColor};">
              <i class="fa-solid fa-water"></i>
            </div>
            <span class="absolute -top-1 -right-1 w-2.5 h-2.5 rounded-full ${isSevere ? 'bg-red-400 animate-ping' : 'bg-blue-400'}"></span>
          </div>
        `,
        iconSize: [24, 24],
        iconAnchor: [12, 12]
      });

      const marker = L.marker(d.center, { icon });
      marker.bindPopup(`
        <div class="p-1 space-y-1 text-xs min-w-[200px]">
          <div class="font-bold text-sm text-white border-b border-slate-700 pb-1 flex items-center justify-between">
            <span>${d.name}</span>
          </div>
          <div class="text-[11px] text-blue-300"><strong>Basin:</strong> ${d.river}</div>
          <div class="text-[11px] text-slate-300"><strong>CWC Gauge:</strong> ${d.cwc_gauge_station}</div>
          <div class="text-[11px] text-amber-300"><strong>Danger Level:</strong> ${d.danger_level_m}m</div>
          <div class="text-[11px] text-slate-400"><strong>Risk Profile:</strong> ${d.annual_flood_frequency || 'Monitored'}</div>
          <button class="mt-2 w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-1.5 px-2 rounded text-xs transition" onclick="window.selectDistrictById('${d.id}')">
            <i class="fa-solid fa-satellite-dish mr-1"></i> Analyze This Region
          </button>
        </div>
      `);
      this.allIndiaLayer.addLayer(marker);
    });
  }
}
