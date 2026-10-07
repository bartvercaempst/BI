import json
import os
import sys

def build_map_html(locations, bundels):
    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DB Cargo Belgium — Bedieningen & Moederbundels Satellietkaart</title>
  
  <!-- Google Fonts: Nunito -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Nunito:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400;1,700&display=swap" rel="stylesheet">

  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Nunito', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }}
    body {{
      font-family: 'Nunito', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
      background: #0f172a;
      color: #e2e8f0;
      overflow: hidden;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }}
    button, input, select, textarea, .leaflet-container, .leaflet-tooltip {{
      font-family: 'Nunito', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }}

    /* Header Bar */
    header {{
      background: #090d16;
      border-bottom: 1px solid #1e293b;
      height: 64px;
      padding: 0 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      z-index: 1000;
      flex-shrink: 0;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .db-logo {{
      background: #e01e2b;
      color: white;
      font-weight: 900;
      font-size: 14px;
      padding: 4px 9px;
      border-radius: 4px;
      letter-spacing: 0.5px;
      box-shadow: 0 2px 6px rgba(224, 30, 43, 0.4);
    }}
    .brand-titles h1 {{
      font-size: 16px;
      font-weight: 800;
      color: #f8fafc;
      letter-spacing: -0.2px;
    }}
    .brand-titles p {{
      font-size: 11px;
      color: #94a3b8;
      font-weight: 500;
    }}

    .header-center {{
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .hub-btn {{
      background: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}
    .hub-btn:hover {{
      background: #334155;
      color: #ffffff;
      border-color: #64748b;
    }}
    .hub-btn.active {{
      background: #e01e2b;
      color: #ffffff;
      border-color: #e01e2b;
      box-shadow: 0 0 10px rgba(224, 30, 43, 0.4);
    }}

    .header-right {{
      display: flex;
      align-items: center;
      gap: 8px;
    }}

    /* Server sync indicator */
    .sync-status-indicator {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 600;
      padding: 4px 9px;
      border-radius: 20px;
      background: #1e293b;
      border: 1px solid #334155;
      color: #94a3b8;
    }}
    .sync-dot {{
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #f59e0b;
    }}
    .sync-dot.connected {{
      background: #10b981;
      box-shadow: 0 0 6px #10b981;
    }}

    /* Modified Coordinates Badge */
    .saved-count-pill {{
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.5);
      color: #fbbf24;
      font-size: 11px;
      font-weight: 700;
      padding: 5px 10px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: all 0.15s;
    }}
    .saved-count-pill:hover {{
      background: rgba(245, 158, 11, 0.25);
    }}

    .btn-header-action {{
      background: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
      padding: 6px 11px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s;
      display: flex;
      align-items: center;
      gap: 5px;
    }}
    .btn-header-action:hover {{
      background: #334155;
      color: white;
    }}

    .layer-selector {{
      display: flex;
      background: #1e293b;
      padding: 3px;
      border-radius: 8px;
      border: 1px solid #334155;
    }}
    .layer-opt {{
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 8px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .layer-opt:hover {{
      color: #e2e8f0;
    }}
    .layer-opt.active {{
      background: #0ea5e9;
      color: #ffffff;
      box-shadow: 0 1px 4px rgba(0,0,0,0.3);
    }}

    /* Main Container */
    .main-container {{
      flex: 1;
      display: flex;
      position: relative;
      overflow: hidden;
    }}

    /* Floating Alert Banner (During Drag or Point-Pick mode) */
    .action-banner {{
      position: absolute;
      top: 14px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.96);
      border: 2px solid #38bdf8;
      border-radius: 8px;
      padding: 8px 16px;
      color: #f8fafc;
      font-size: 12px;
      z-index: 1200;
      display: none;
      align-items: center;
      gap: 12px;
      box-shadow: 0 6px 20px rgba(0,0,0,0.7);
      animation: fadeInDown 0.2s ease-out;
    }}
    .action-banner.active {{
      display: flex;
    }}
    @keyframes fadeInDown {{
      from {{ opacity: 0; transform: translate(-50%, -10px); }}
      to {{ opacity: 1; transform: translate(-50%, 0); }}
    }}
    .action-banner-btn {{
      background: #38bdf8;
      color: #0f172a;
      border: none;
      padding: 4px 10px;
      border-radius: 4px;
      font-weight: 800;
      font-size: 11px;
      cursor: pointer;
    }}
    .action-banner-cancel {{
      background: transparent;
      color: #94a3b8;
      border: 1px solid #475569;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 11px;
      cursor: pointer;
    }}

    /* Toast Notification */
    .toast-notification {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #0f172a;
      border: 1px solid #10b981;
      color: #f1f5f9;
      padding: 12px 18px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      z-index: 2000;
      box-shadow: 0 10px 25px rgba(0,0,0,0.6);
      display: flex;
      align-items: center;
      gap: 8px;
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.25s ease;
      pointer-events: none;
    }}
    .toast-notification.active {{
      transform: translateY(0);
      opacity: 1;
    }}
    .toast-notification.toast-warn {{
      border-color: #f59e0b;
    }}

    /* Sidebar */
    .sidebar {{
      width: 390px;
      background: #090d16;
      border-right: 1px solid #1e293b;
      display: flex;
      flex-direction: column;
      z-index: 900;
      transition: transform 0.25s ease;
      flex-shrink: 0;
    }}
    .sidebar.collapsed {{
      transform: translateX(-390px);
      margin-right: -390px;
    }}
    .sidebar-header {{
      padding: 12px 16px;
      border-bottom: 1px solid #1e293b;
      background: #0f172a;
    }}
    .search-input-wrap {{
      position: relative;
      margin-bottom: 8px;
    }}
    .search-input {{
      width: 100%;
      background: #1e293b;
      border: 1px solid #334155;
      color: #f1f5f9;
      border-radius: 6px;
      padding: 8px 12px 8px 34px;
      font-size: 12px;
      outline: none;
      transition: border-color 0.15s;
    }}
    .search-input:focus {{
      border-color: #38bdf8;
    }}
    .search-icon {{
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
      color: #64748b;
      pointer-events: none;
    }}

    .filter-tabs {{
      display: flex;
      gap: 5px;
      flex-wrap: wrap;
    }}
    .filter-chip {{
      background: #1e293b;
      border: 1px solid #334155;
      color: #94a3b8;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 600;
      padding: 3px 9px;
      cursor: pointer;
      transition: all 0.15s;
    }}
    .filter-chip:hover {{
      background: #334155;
      color: #e2e8f0;
    }}
    .filter-chip.active {{
      background: #2563eb;
      color: #ffffff;
      border-color: #2563eb;
    }}
    .filter-chip.chip-green.active {{
      background: #059669;
      border-color: #059669;
    }}
    .filter-chip.chip-red.active {{
      background: #dc2626;
      border-color: #dc2626;
    }}
    .filter-chip.chip-gold.active {{
      background: #d97706;
      border-color: #d97706;
    }}

    .sidebar-stats {{
      padding: 7px 16px;
      background: #090d16;
      border-bottom: 1px solid #1e293b;
      font-size: 11px;
      font-weight: 600;
      color: #64748b;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}

    .locations-list {{
      flex: 1;
      overflow-y: auto;
      padding: 8px;
    }}
    .locations-list::-webkit-scrollbar {{
      width: 6px;
    }}
    .locations-list::-webkit-scrollbar-thumb {{
      background: #334155;
      border-radius: 3px;
    }}

    .loc-card {{
      background: #0f172a;
      border: 1px solid #1e293b;
      border-radius: 8px;
      padding: 10px 12px;
      margin-bottom: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      position: relative;
    }}
    .loc-card:hover {{
      border-color: #475569;
      background: #1e293b;
    }}
    .loc-card.selected {{
      border-color: #38bdf8;
      background: #1e293b;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.25);
    }}
    .loc-card-header {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 6px;
      margin-bottom: 4px;
    }}
    .loc-card-title {{
      font-size: 13px;
      font-weight: 700;
      color: #f8fafc;
      line-height: 1.3;
    }}
    .loc-status-badge {{
      font-size: 10px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 4px;
      white-space: nowrap;
      flex-shrink: 0;
    }}
    .badge-bi-yes {{
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }}
    .badge-bi-no {{
      background: rgba(239, 68, 68, 0.15);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.4);
    }}
    .badge-bundel {{
      background: rgba(245, 158, 11, 0.15);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.4);
    }}
    .badge-custom-coord {{
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.4);
      font-size: 9px;
      font-weight: 700;
      padding: 1px 4px;
      border-radius: 3px;
    }}

    .loc-card-details {{
      font-size: 11px;
      color: #94a3b8;
      line-height: 1.4;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }}
    
    /* Alias chip list in card */
    .loc-card-aliases {{
      display: flex;
      align-items: center;
      gap: 4px;
      margin-top: 4px;
      font-size: 10px;
      color: #38bdf8;
      flex-wrap: wrap;
    }}
    .loc-card-aliases-tag {{
      background: rgba(56, 189, 248, 0.12);
      border: 1px solid rgba(56, 189, 248, 0.3);
      padding: 1px 5px;
      border-radius: 3px;
    }}

    .loc-card-meta {{
      display: flex;
      align-items: center;
      gap: 6px;
      margin-top: 5px;
      font-size: 10px;
      color: #64748b;
    }}
    .loc-card-meta span {{
      background: #1e293b;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
    }}

    /* Map Area */
    #map {{
      flex: 1;
      height: 100%;
      background: #0b1120;
    }}

    /* Sidebar Toggle Button */
    .sidebar-toggle {{
      position: absolute;
      top: 14px;
      left: 14px;
      z-index: 800;
      background: #0f172a;
      border: 1px solid #334155;
      color: #cbd5e1;
      width: 34px;
      height: 34px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 4px 10px rgba(0,0,0,0.5);
      transition: all 0.15s;
    }}
    .sidebar-toggle:hover {{
      background: #1e293b;
      color: white;
      border-color: #64748b;
    }}

    /* Floating Legend */
    .map-legend {{
      position: absolute;
      bottom: 20px;
      left: 20px;
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(8px);
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 10px 14px;
      z-index: 800;
      font-size: 11px;
      display: flex;
      flex-direction: column;
      gap: 6px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.5);
      pointer-events: auto;
    }}
    .legend-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      color: #cbd5e1;
      font-weight: 600;
    }}
    .legend-dot {{
      width: 14px;
      height: 14px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 9px;
      font-weight: bold;
      color: white;
      flex-shrink: 0;
    }}
    .legend-dot.green {{
      background: #10b981;
      box-shadow: 0 0 6px rgba(16, 185, 129, 0.6);
    }}
    .legend-dot.red {{
      background: #ef4444;
      box-shadow: 0 0 6px rgba(239, 68, 68, 0.6);
    }}
    .legend-dot.gold {{
      background: #f59e0b;
      box-shadow: 0 0 6px rgba(245, 158, 11, 0.6);
    }}
    .legend-line {{
      width: 16px;
      height: 4px;
      border-radius: 2px;
      background: #eab308;
    }}

    /* Floating Detail Card */
    .detail-overlay {{
      position: absolute;
      top: 14px;
      right: 14px;
      width: 410px;
      max-height: calc(100% - 28px);
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(12px);
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 18px;
      z-index: 850;
      box-shadow: 0 10px 30px rgba(0,0,0,0.7);
      display: none;
      flex-direction: column;
      overflow-y: auto;
    }}
    .detail-overlay.active {{
      display: flex;
    }}
    .detail-overlay::-webkit-scrollbar {{
      width: 5px;
    }}
    .detail-overlay::-webkit-scrollbar-thumb {{
      background: #475569;
      border-radius: 3px;
    }}
    .detail-close {{
      position: absolute;
      top: 14px;
      right: 14px;
      background: #1e293b;
      border: 1px solid #334155;
      color: #94a3b8;
      width: 26px;
      height: 26px;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
      transition: all 0.15s;
    }}
    .detail-close:hover {{
      color: white;
      background: #334155;
    }}
    .detail-header {{
      margin-bottom: 12px;
      padding-right: 28px;
    }}
    .detail-status-pill {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 8px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 800;
      margin-bottom: 6px;
    }}
    .detail-title {{
      font-size: 18px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.25;
    }}
    .detail-subtitle {{
      font-size: 12px;
      color: #94a3b8;
      margin-top: 3px;
      font-weight: 600;
    }}

    .detail-grid {{
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 10px;
    }}
    .detail-item {{
      background: rgba(30, 41, 59, 0.7);
      border: 1px solid #334155;
      border-radius: 8px;
      padding: 9px 12px;
    }}
    .detail-item-label {{
      font-size: 10px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: #64748b;
      margin-bottom: 3px;
    }}
    .detail-item-val {{
      font-size: 12px;
      color: #f1f5f9;
      line-height: 1.4;
      font-weight: 500;
    }}

    /* ========================================= */
    /* ALIASES & LINKING STYLES (TASK 2)         */
    /* ========================================= */
    .alias-section {{
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid #0284c7;
      border-radius: 8px;
      padding: 11px 12px;
    }}
    .alias-section-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 6px;
    }}
    .alias-section-header .detail-item-label {{
      color: #38bdf8;
      font-size: 11px;
    }}
    .alias-count-tag {{
      font-size: 10px;
      background: rgba(56, 189, 248, 0.15);
      color: #38bdf8;
      padding: 1px 6px;
      border-radius: 10px;
      font-weight: 700;
    }}
    .alias-chips-wrap {{
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      margin-bottom: 8px;
      min-height: 22px;
    }}
    .alias-chip {{
      background: #1e293b;
      border: 1px solid #475569;
      color: #f1f5f9;
      font-size: 11px;
      font-weight: 600;
      padding: 2px 7px;
      border-radius: 4px;
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }}
    .alias-chip-del {{
      background: transparent;
      border: none;
      color: #94a3b8;
      cursor: pointer;
      font-size: 12px;
      line-height: 1;
      padding: 0;
      display: inline-flex;
      align-items: center;
      justify-content: center;
    }}
    .alias-chip-del:hover {{
      color: #f87171;
    }}
    .alias-controls-box {{
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin-top: 6px;
      border-top: 1px solid #1e293b;
      padding-top: 6px;
    }}
    .alias-add-row {{
      display: flex;
      gap: 6px;
    }}
    .alias-input {{
      flex: 1;
      background: #1e293b;
      border: 1px solid #334155;
      color: #ffffff;
      border-radius: 5px;
      padding: 5px 8px;
      font-size: 11px;
      outline: none;
    }}
    .alias-input:focus {{
      border-color: #38bdf8;
    }}
    .btn-alias-add {{
      background: #0284c7;
      color: white;
      border: none;
      border-radius: 5px;
      padding: 5px 9px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.15s;
      white-space: nowrap;
    }}
    .btn-alias-add:hover {{
      background: #0369a1;
    }}
    .alias-merge-row {{
      display: flex;
      gap: 6px;
    }}
    .merge-select {{
      flex: 1;
      background: #1e293b;
      border: 1px solid #334155;
      color: #cbd5e1;
      border-radius: 5px;
      padding: 5px 6px;
      font-size: 11px;
      outline: none;
    }}
    .btn-alias-merge {{
      background: #475569;
      color: white;
      border: none;
      border-radius: 5px;
      padding: 5px 9px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.15s;
      white-space: nowrap;
    }}
    .btn-alias-merge:hover {{
      background: #64748b;
    }}

    /* Editable GPS Coordinates Box */
    .edit-coord-box {{
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid #3b82f6;
      border-radius: 8px;
      padding: 10px 12px;
      margin-top: 4px;
    }}
    .edit-coord-title {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }}
    .edit-coord-title span {{
      font-size: 11px;
      font-weight: 800;
      color: #93c5fd;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }}
    .coord-inputs-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 8px;
    }}
    .coord-field label {{
      display: block;
      font-size: 10px;
      font-weight: 600;
      color: #94a3b8;
      margin-bottom: 3px;
    }}
    .coord-input {{
      width: 100%;
      background: #1e293b;
      border: 1px solid #475569;
      color: #ffffff;
      border-radius: 5px;
      padding: 6px 8px;
      font-size: 12px;
      font-family: monospace;
      outline: none;
      transition: border-color 0.15s;
    }}
    .coord-input:focus {{
      border-color: #38bdf8;
    }}

    .coord-tools-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6px;
      margin-bottom: 8px;
    }}
    .btn-coord-tool {{
      background: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
      padding: 6px;
      border-radius: 5px;
      font-size: 11px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      transition: all 0.15s;
    }}
    .btn-coord-tool:hover {{
      background: #334155;
      color: white;
    }}
    .btn-coord-tool.active {{
      background: #0284c7;
      color: white;
      border-color: #38bdf8;
      box-shadow: 0 0 8px rgba(56, 189, 248, 0.4);
    }}

    .coord-save-row {{
      display: flex;
      gap: 6px;
    }}
    .btn-coord-save {{
      flex: 2;
      background: #10b981;
      color: white;
      border: none;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 5px;
      transition: background 0.15s;
    }}
    .btn-coord-save:hover {{
      background: #059669;
    }}
    .btn-coord-reset {{
      flex: 1;
      background: #1e293b;
      color: #94a3b8;
      border: 1px solid #334155;
      padding: 8px 8px;
      border-radius: 6px;
      font-size: 10px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
      text-align: center;
    }}
    .btn-coord-reset:hover {{
      color: white;
      border-color: #64748b;
    }}

    .detail-actions {{
      margin-top: 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .btn-action-secondary {{
      background: #1e293b;
      color: #93c5fd;
      border: 1px solid #3b82f6;
      padding: 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
      cursor: pointer;
      text-align: center;
      text-decoration: none;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: background 0.15s;
    }}
    .btn-action-secondary:hover {{
      background: #1e3a8a;
      color: white;
    }}

    /* Custom Leaflet Marker Pins - FIXED SIZE & ANCHOR (ZERO HOVER JITTER & ZERO ZOOM DRIFT) */
    .leaflet-marker-icon.custom-marker,
    .custom-marker {{
      position: absolute !important;
      cursor: pointer;
      background: transparent !important;
      border: none !important;
    }}
    .marker-pin {{
      width: 26px;
      height: 26px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      font-size: 11px;
      color: #ffffff;
      border: 2px solid #ffffff;
      box-shadow: 0 2px 8px rgba(0,0,0,0.6);
      transition: box-shadow 0.15s ease, border-color 0.15s ease;
      background-clip: padding-box;
    }}
    .marker-pin:hover {{
      box-shadow: 0 0 12px #ffffff, 0 2px 8px rgba(0,0,0,0.8);
    }}
    .marker-pin.pin-green {{
      background: #10b981;
    }}
    .marker-pin.pin-red {{
      background: #ef4444;
    }}
    .marker-pin.pin-gold {{
      background: #f59e0b;
      border-radius: 4px;
      transform: rotate(45deg);
    }}
    .marker-pin.pin-gold span {{
      transform: rotate(-45deg);
    }}
    
    /* When marker is being actively dragged */
    .custom-marker.is-being-dragged .marker-pin {{
      border-color: #38bdf8;
      box-shadow: 0 0 16px #38bdf8, 0 0 28px rgba(56, 189, 248, 0.8) !important;
      transform: scale(1.15);
    }}
    .custom-marker.has-custom-coord::after {{
      content: '';
      position: absolute;
      top: -3px;
      right: -3px;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #38bdf8;
      border: 1px solid #0f172a;
    }}

    .marker-pulse {{
      position: absolute;
      top: -3px;
      left: -3px;
      right: -3px;
      bottom: -3px;
      border-radius: 50%;
      border: 2px solid rgba(239, 68, 68, 0.7);
      animation: markerPulse 2s infinite ease-out;
      pointer-events: none;
    }}
    @keyframes markerPulse {{
      0% {{ transform: scale(1); opacity: 0.9; }}
      100% {{ transform: scale(1.8); opacity: 0; }}
    }}

    /* Permanent Label Tag */
    .marker-label-tag {{
      position: absolute;
      top: 28px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 23, 42, 0.92);
      border: 1px solid #334155;
      color: #f1f5f9;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      white-space: nowrap;
      pointer-events: none;
      box-shadow: 0 2px 6px rgba(0,0,0,0.6);
      z-index: 10;
      display: none;
    }}
    body.show-labels .marker-label-tag {{
      display: block;
    }}

    /* Leaflet Tooltip Custom Styling */
    .leaflet-tooltip-pane .leaflet-tooltip.custom-tip {{
      background: rgba(15, 23, 42, 0.95);
      border: 1px solid #38bdf8;
      border-radius: 6px;
      color: #ffffff;
      padding: 4px 8px;
      font-size: 11px;
      font-weight: 700;
      box-shadow: 0 4px 12px rgba(0,0,0,0.6);
    }}
    .leaflet-tooltip-pane .leaflet-tooltip.custom-tip::before {{
      border-top-color: #38bdf8;
    }}

    /* Modal Overlay */
    .modal-backdrop {{
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(4px);
      z-index: 3000;
      display: none;
      align-items: center;
      justify-content: center;
    }}
    .modal-backdrop.active {{
      display: flex;
    }}
    .modal-box {{
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 12px;
      width: 520px;
      max-width: 90vw;
      padding: 24px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.8);
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}
    .modal-box h2 {{
      font-size: 18px;
      font-weight: 800;
      color: #f8fafc;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .modal-close {{
      background: transparent;
      border: none;
      color: #94a3b8;
      font-size: 18px;
      cursor: pointer;
    }}
    .modal-body {{
      font-size: 13px;
      color: #cbd5e1;
      line-height: 1.5;
    }}
    .modal-body ul {{
      margin: 10px 0 10px 20px;
    }}
    .modal-actions {{
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-top: 10px;
    }}
    .btn-modal-action {{
      background: #1e293b;
      border: 1px solid #334155;
      color: #f1f5f9;
      padding: 10px 14px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: all 0.15s;
    }}
    .btn-modal-action:hover {{
      background: #334155;
      border-color: #64748b;
    }}
    .btn-modal-primary {{
      background: #2563eb;
      border-color: #3b82f6;
    }}
    .btn-modal-primary:hover {{
      background: #1d4ed8;
    }}
    .btn-modal-danger {{
      background: rgba(239, 68, 68, 0.1);
      border-color: rgba(239, 68, 68, 0.3);
      color: #f87171;
    }}
    .btn-modal-danger:hover {{
      background: rgba(239, 68, 68, 0.2);
    }}

    /* Responsive */
    @media (max-width: 900px) {{
      .sidebar {{
        width: 100%;
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
      }}
      .detail-overlay {{
        width: calc(100% - 28px);
      }}
      .header-center {{
        display: none;
      }}
    }}
  </style>
</head>
<body class="show-labels">

  <!-- Top Header Navigation -->
  <header>
    <div class="brand">
      <span class="db-logo">DB</span>
      <div class="brand-titles">
        <h1>DB Cargo Belgium — West-Vlaanderen Bedieningen</h1>
        <p>Satellietkaart met Private Aansluitingen & Moederbundels</p>
      </div>
    </div>

    <!-- Quick Hub Jump Buttons -->
    <div class="header-center">
      <button class="hub-btn active" onclick="zoomToHub('wvl', this)">🌐 Heel West-Vlaanderen</button>
      <button class="hub-btn" onclick="zoomToHub('zeebrugge', this)">⚓ Zeebrugge Haven</button>
      <button class="hub-btn" onclick="zoomToHub('oostende', this)">🌊 Oostende & Plassendale</button>
      <button class="hub-btn" onclick="zoomToHub('brugge', this)">🏰 Brugge & Roeselare</button>
      <button class="hub-btn" onclick="zoomToHub('kortrijk', this)">🏭 Kortrijk & Lauwe</button>
    </div>

    <!-- Right Controls: Status, Labels, Layer, Coordinates Manager -->
    <div class="header-right">
      <!-- Sync Status -->
      <div class="sync-status-indicator" id="syncStatusBox" title="Status van opslag">
        <span class="sync-dot" id="syncStatusDot"></span>
        <span id="syncStatusText">Browser Opslag</span>
      </div>

      <!-- Modified counter pill -->
      <div class="saved-count-pill" id="savedCountPill" style="display:none;" onclick="openExportModal()" title="Klik om opgeslagen wijzigingen te bekijken en exporteren">
        ✏️ <span id="savedCountNum">0</span> gewijzigd
      </div>

      <!-- Export / Manager Button -->
      <button class="btn-header-action" onclick="openExportModal()" title="Beheer & Exporteer Coördinaten">
        💾 Coördinaten Beheer
      </button>

      <button id="toggleLabelsBtn" class="btn-header-action active" onclick="toggleLabels()">🏷️ Labels Aan</button>

      <div class="layer-selector">
        <button class="layer-opt active" id="btnLayerSat" onclick="setBaseLayer('sat')">🛰️ Satelliet</button>
        <button class="layer-opt active" id="btnLayerRail" onclick="toggleRailLayer()">🚆 Sporen</button>
        <button class="layer-opt" id="btnLayerStreet" onclick="setBaseLayer('street')">🗺️ Kaart</button>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <div class="main-container">
    
    <!-- Floating Drag Action Banner -->
    <div class="action-banner" id="actionBanner">
      <span id="actionBannerText">📍 Sleep de marker naar het gewenste spoor op de satelliet en klik op <strong>'Positie Opslaan'</strong>.</span>
      <button class="action-banner-btn" onclick="saveCurrentCoords()">💾 Nu Opslaan</button>
      <button class="action-banner-cancel" onclick="cancelInteractiveTool()">Annuleren</button>
    </div>

    <!-- Toast Notification -->
    <div class="toast-notification" id="toastNotification">
      <span id="toastIcon">✓</span>
      <span id="toastMessage">Actie voltooid</span>
    </div>

    <!-- Sidebar: Search & Filterable List -->
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <div class="search-input-wrap">
          <svg class="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
          <input type="text" id="searchInput" class="search-input" placeholder="Zoek op naam, alias (bijv. ECS 1), spoor..." oninput="handleFilter()" />
        </div>
        <div class="filter-tabs">
          <button class="filter-chip active" id="filterAll" onclick="setFilter('all', this)">Alle</button>
          <button class="filter-chip chip-green" id="filterBiYes" onclick="setFilter('bi-yes', this)">🟢 Reeds BI</button>
          <button class="filter-chip chip-red" id="filterBiNo" onclick="setFilter('bi-no', this)">🔴 Nog geen BI</button>
          <button class="filter-chip chip-gold" id="filterBundels" onclick="setFilter('bundel', this)">🟡 Bundels</button>
        </div>
      </div>

      <div class="sidebar-stats">
        <span id="resultCount">Laden...</span>
        <span>West-Vlaanderen Zone</span>
      </div>

      <div class="locations-list" id="locationsList">
        <!-- Rendered via JS -->
      </div>
    </aside>

    <!-- Sidebar Toggle -->
    <button class="sidebar-toggle" onclick="toggleSidebar()" title="Toggle lijst">
      <svg id="toggleIcon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
    </button>

    <!-- Leaflet Map Container -->
    <div id="map"></div>

    <!-- Map Legend -->
    <div class="map-legend">
      <div class="legend-row">
        <div class="legend-dot green">✓</div>
        <span id="legBiYesText">Reeds een BI</span>
      </div>
      <div class="legend-row">
        <div class="legend-dot red">!</div>
        <span id="legBiNoText">Nog GEEN BI</span>
      </div>
      <div class="legend-row">
        <div class="legend-dot gold">◆</div>
        <span>Infrabel Moederbundels (rangeerterreinen)</span>
      </div>
      <div class="legend-row" id="railLegendRow" style="display: flex;">
        <div class="legend-line"></div>
        <span>OpenRailwayMap spoorweginfrastructuur</span>
      </div>
    </div>

    <!-- Floating Detail Card -->
    <div class="detail-overlay" id="detailOverlay">
      <button class="detail-close" onclick="closeDetail()">&times;</button>
      <div class="detail-header">
        <div id="detailStatusPill" class="detail-status-pill badge-bi-yes">✓ BI BESCHIKBAAR</div>
        <h2 id="detailTitle" class="detail-title">Locatie</h2>
        <div id="detailSubtitle" class="detail-subtitle">Zone info</div>
      </div>

      <div class="detail-grid">
        
        <!-- SECTION: Gekoppelde Benamingen & Aliassen (TASK 2) -->
        <div class="detail-item alias-section" id="detailAliasSection">
          <div class="alias-section-header">
            <div class="detail-item-label">🔗 Gekoppelde Benamingen (1 BI voor allen)</div>
            <span class="alias-count-tag" id="detailAliasCount">0 synoniemen</span>
          </div>
          <div id="detailAliasesContainer" class="alias-chips-wrap">
            <!-- Chips rendered dynamically -->
          </div>
          <div class="alias-controls-box">
            <div class="alias-add-row">
              <input type="text" id="newAliasInput" class="alias-input" placeholder="Voeg synoniem toe (bijv. SA ECS 1)..." onkeydown="if(event.key==='Enter') addCurrentAlias()" />
              <button class="btn-alias-add" onclick="addCurrentAlias()">+ Voeg toe</button>
            </div>
            <div class="alias-merge-row">
              <select id="mergeLocationSelect" class="merge-select">
                <option value="">-- Koppel met andere bediening --</option>
              </select>
              <button class="btn-alias-merge" onclick="mergeSelectedLocation()">🔗 Koppel</button>
            </div>
          </div>
        </div>

        <!-- Editable GPS Coordinates Box -->
        <div class="edit-coord-box">
          <div class="edit-coord-title">
            <span>📍 GPS Coördinaten (Aanpasbaar)</span>
            <span id="coordCustomBadge" class="badge-custom-coord" style="display:none;">HANDMATIG AANGEPAST</span>
          </div>
          
          <div class="coord-inputs-row">
            <div class="coord-field">
              <label>Breedtegraad (Lat):</label>
              <input type="number" step="0.000001" id="editLat" class="coord-input" onchange="onManualCoordInputChange()" />
            </div>
            <div class="coord-field">
              <label>Lengtegraad (Lng):</label>
              <input type="number" step="0.000001" id="editLng" class="coord-input" onchange="onManualCoordInputChange()" />
            </div>
          </div>

          <div class="coord-tools-row">
            <button id="btnDragMarker" class="btn-coord-tool" onclick="toggleDragCurrentMarker()">
              <span>🎯</span> <span id="btnDragText">Marker Verslepen</span>
            </button>
            <button id="btnPickPoint" class="btn-coord-tool" onclick="togglePickPoint()">
              <span>📍</span> <span id="btnPickText">Prikken op Kaart</span>
            </button>
          </div>

          <div class="coord-save-row">
            <button class="btn-coord-save" onclick="saveCurrentCoords()">
              <span>💾</span> Positie Opslaan
            </button>
            <button id="btnResetCoords" class="btn-coord-reset" onclick="resetCurrentCoords()" title="Herstel de fabrieksinstelling van dit item">
              Herstel Origineel
            </button>
          </div>
        </div>

        <div class="detail-item">
          <div class="detail-item-label">Moederbundel (Infrabel)</div>
          <div id="detailMoederbundel" class="detail-item-val">-</div>
        </div>
        <div class="detail-item">
          <div class="detail-item-label">Bedieningssporen & Lengte</div>
          <div id="detailSporen" class="detail-item-val">-</div>
        </div>
        <div class="detail-item">
          <div class="detail-item-label">Adres & Toegangsweg</div>
          <div id="detailAdres" class="detail-item-val">-</div>
        </div>
        <div class="detail-item">
          <div class="detail-item-label">Beveiliging & Wissels</div>
          <div id="detailBeveiliging" class="detail-item-val">-</div>
        </div>
        <div class="detail-item">
          <div class="detail-item-label">PPGI Bronreferentie</div>
          <div id="detailPpgi" class="detail-item-val">-</div>
        </div>
      </div>

      <div class="detail-actions">
        <a id="detailNavBtn" href="#" target="_blank" class="btn-action-secondary">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="3 11 22 2 13 21 11 13 3 11"></polygon></svg>
          Open in Google Maps Satelliet
        </a>
      </div>
    </div>

  </div>

  <!-- Modal: Export & Coördinaten Beheer -->
  <div class="modal-backdrop" id="exportModal">
    <div class="modal-box">
      <h2>
        <span>💾 Coördinaten Beheer & Back-up</span>
        <button class="modal-close" onclick="closeExportModal()">&times;</button>
      </h2>
      <div class="modal-body">
        <p>Alle handmatig verplaatste GPS coördinaten en gekoppelde synoniemen worden <strong>automatisch bewaard</strong> in je browser (LocalStorage). Zelfs na herladen blijven al je aanpassingen behouden.</p>
        <div style="margin: 12px 0; background: #1e293b; padding: 10px 14px; border-radius: 6px; border: 1px solid #334155;">
          <strong>Huidige status:</strong> <span id="modalCustomCount">0</span> locaties handmatig aangepast.
        </div>
        <p>Gebruik onderstaande knoppen om je gegevens te exporteren of over te dragen naar GitHub:</p>
      </div>
      <div class="modal-actions">
        <button class="btn-modal-action btn-modal-primary" onclick="downloadUpdatedJson()">
          📥 Download bijgewerkte 'locs_gps.json' (inclusief aliassen)
        </button>
        <button class="btn-modal-action" onclick="downloadUpdatedHtml()">
          📄 Download complete 'kaart_bedieningen.html'
        </button>
        <button class="btn-modal-action" onclick="copyModifiedCoordsToClipboard()">
          📋 Kopieer gewijzigde coördinaten naar klembord
        </button>
        <button class="btn-modal-action btn-modal-danger" onclick="resetAllOverrides()">
          ⚠️ Wis alle handmatige aanpassingen (Herstel fabrieksinstellingen)
        </button>
      </div>
    </div>
  </div>

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <script>
    // Embedded Base Data
    const rawLocations = {json.dumps(locations, ensure_ascii=False)};
    const rawBundels = {json.dumps(bundels, ensure_ascii=False)};

    // Local Storage Keys
    const STORAGE_KEY = 'db_cargo_saved_coords_v1';
    const STORAGE_ALIASES_KEY = 'db_cargo_saved_aliases_v1';
    const STORAGE_MERGED_KEY = 'db_cargo_saved_merged_v1';

    // Hub extents
    const HUB_COORDS = {{
      'wvl': {{ center: [51.15, 3.12], zoom: 10 }},
      'zeebrugge': {{ center: [51.325, 3.21], zoom: 13 }},
      'oostende': {{ center: [51.215, 3.00], zoom: 13 }},
      'brugge': {{ center: [51.15, 3.18], zoom: 12 }},
      'kortrijk': {{ center: [50.82, 3.25], zoom: 12 }}
    }};

    // State
    let currentFilter = 'all';
    let activeMarkerId = null;
    let markersMap = {{}};
    let isDraggingActive = false;
    let isPickPointActive = false;
    let serverAvailable = false;

    // Load persisted overrides from LocalStorage
    function loadPersistedOverrides() {{
      try {{
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : {{}};
      }} catch (e) {{
        return {{}};
      }}
    }}

    function savePersistedOverrides(overrides) {{
      try {{
        localStorage.setItem(STORAGE_KEY, JSON.stringify(overrides));
      }} catch (e) {{}}
      updateCustomCountBadge();
    }}

    function loadPersistedAliases() {{
      try {{
        const raw = localStorage.getItem(STORAGE_ALIASES_KEY);
        return raw ? JSON.parse(raw) : {{}};
      }} catch (e) {{
        return {{}};
      }}
    }}

    function savePersistedAliases(aliasesMap) {{
      try {{
        localStorage.setItem(STORAGE_ALIASES_KEY, JSON.stringify(aliasesMap));
      }} catch (e) {{}}
    }}

    // Check optional local Python server on port 8055
    async function checkServerStatus() {{
      try {{
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 1200);
        const res = await fetch('http://localhost:8055/api/status', {{ signal: controller.signal }});
        clearTimeout(timeoutId);
        if (res.ok) {{
          serverAvailable = true;
          document.getElementById('syncStatusDot').classList.add('connected');
          document.getElementById('syncStatusText').textContent = 'Server Actief (Auto-Save)';
          return;
        }}
      }} catch (e) {{}}
      serverAvailable = false;
      document.getElementById('syncStatusDot').classList.remove('connected');
      document.getElementById('syncStatusText').textContent = 'Browser Opslag (Actief)';
    }}

    // Leaflet Layers
    const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
      maxZoom: 19,
      attribution: 'Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics'
    }});

    const esriLabels = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{{z}}/{{y}}/{{x}}', {{
      maxZoom: 19
    }});

    const streetLayer = L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{y}}/{{x}}{{r}}.png', {{
      maxZoom: 19,
      attribution: '&copy; CartoDB &copy; OpenStreetMap'
    }});

    const railLayer = L.tileLayer('https://{{s}}.tiles.openrailwaymap.org/standard/{{z}}/{{x}}/{{y}}.png', {{
      maxZoom: 19,
      attribution: 'Map style: &copy; OpenRailwayMap'
    }});

    // Initialize Map
    const map = L.map('map', {{
      center: [51.15, 3.12],
      zoom: 10,
      layers: [esriSatellite, esriLabels, railLayer],
      zoomControl: false
    }});

    L.control.zoom({{ position: 'bottomright' }}).addTo(map);

    let railLayerActive = true;
    let baseMode = 'sat';

    function setBaseLayer(mode) {{
      baseMode = mode;
      document.getElementById('btnLayerSat').classList.toggle('active', mode === 'sat');
      document.getElementById('btnLayerStreet').classList.toggle('active', mode === 'street');

      if (mode === 'sat') {{
        map.removeLayer(streetLayer);
        map.addLayer(esriSatellite);
        map.addLayer(esriLabels);
        if (railLayerActive) map.addLayer(railLayer);
      }} else {{
        map.removeLayer(esriSatellite);
        map.removeLayer(esriLabels);
        map.addLayer(streetLayer);
        if (railLayerActive) map.addLayer(railLayer);
      }}
    }}

    function toggleRailLayer() {{
      railLayerActive = !railLayerActive;
      const btn = document.getElementById('btnLayerRail');
      const legRow = document.getElementById('railLegendRow');
      btn.classList.toggle('active', railLayerActive);
      legRow.style.display = railLayerActive ? 'flex' : 'none';

      if (railLayerActive) {{
        map.addLayer(railLayer);
      }} else {{
        map.removeLayer(railLayer);
      }}
    }}

    function toggleLabels() {{
      const b = document.body;
      const btn = document.getElementById('toggleLabelsBtn');
      if (b.classList.contains('show-labels')) {{
        b.classList.remove('show-labels');
        btn.classList.remove('active');
        btn.innerHTML = '🏷️ Labels Uit';
      }} else {{
        b.classList.add('show-labels');
        btn.classList.add('active');
        btn.innerHTML = '🏷️ Labels Aan';
      }}
    }}

    function zoomToHub(hubKey, btn) {{
      document.querySelectorAll('.hub-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      const hub = HUB_COORDS[hubKey];
      if (hub) {{
        map.flyTo(hub.center, hub.zoom, {{ duration: 1.2 }});
      }}
    }}

    // Toast message helper
    let toastTimeout = null;
    function showToast(msg, type = 'success') {{
      const t = document.getElementById('toastNotification');
      const icon = document.getElementById('toastIcon');
      const message = document.getElementById('toastMessage');
      
      message.textContent = msg;
      icon.textContent = type === 'warning' ? '⚠️' : '✓';
      t.className = 'toast-notification active ' + (type === 'warning' ? 'toast-warn' : '');
      
      clearTimeout(toastTimeout);
      toastTimeout = setTimeout(() => {{
        t.classList.remove('active');
      }}, 3500);
    }}

    // Create Marker Icons
    function createMarkerIcon(loc, isCustom) {{
      const customClass = isCustom ? 'has-custom-coord' : '';
      if (loc.is_bundel) {{
        return L.divIcon({{
          className: `custom-marker ${{customClass}}`,
          html: `
            <div class="marker-pin pin-gold">
              <span>◆</span>
            </div>
            <div class="marker-label-tag">${{loc.name}}</div>
          `,
          iconSize: [26, 26],
          iconAnchor: [13, 13]
        }});
      }}

      if (loc.has_bi) {{
        return L.divIcon({{
          className: `custom-marker ${{customClass}}`,
          html: `
            <div class="marker-pin pin-green">
              <span>✓</span>
            </div>
            <div class="marker-label-tag">${{loc.name}}</div>
          `,
          iconSize: [26, 26],
          iconAnchor: [13, 13]
        }});
      }} else {{
        return L.divIcon({{
          className: `custom-marker ${{customClass}}`,
          html: `
            <div class="marker-pulse"></div>
            <div class="marker-pin pin-red">
              <span>!</span>
            </div>
            <div class="marker-label-tag">${{loc.name}}</div>
          `,
          iconSize: [26, 26],
          iconAnchor: [13, 13]
        }});
      }}
    }}

    // Master Items Array
    let allItems = [];
    const persistedCoords = loadPersistedOverrides();
    const persistedAliases = loadPersistedAliases();

    // Populate locations
    rawLocations.forEach(l => {{
      const hasCustom = persistedCoords[l.id] !== undefined;
      const lat = hasCustom ? persistedCoords[l.id].lat : l.lat;
      const lng = hasCustom ? persistedCoords[l.id].lng : l.lng;
      
      // Merge base aliases with any stored aliases
      const storedAliases = persistedAliases[l.id] || [];
      const combinedAliases = Array.from(new Set([...(l.aliases || []), ...storedAliases]));

      allItems.push({{
        id: l.id,
        name: l.name,
        type: l.type || 'Privéaansluiting',
        cluster: l.cluster,
        zone: l.zone,
        zone_name: l.zone_name,
        has_bi: l.has_bi,
        bi_version: l.bi_version,
        moederbundel: l.moederbundel,
        sporen: l.sporen,
        adres: l.adres,
        toegang_weg: l.toegang_weg,
        beveiliging: l.beveiliging,
        ppgi_ref: l.ppgi_ref,
        original_lat: l.lat,
        original_lng: l.lng,
        lat: lat,
        lng: lng,
        aliases: combinedAliases,
        is_custom_coord: hasCustom,
        is_bundel: false
      }});
    }});

    // Populate bundels
    rawBundels.forEach((b, idx) => {{
      const bundelId = 'bundel_' + idx;
      const hasCustom = persistedCoords[bundelId] !== undefined;
      const lat = hasCustom ? persistedCoords[bundelId].lat : b.lat;
      const lng = hasCustom ? persistedCoords[bundelId].lng : b.lng;

      allItems.push({{
        id: bundelId,
        name: b.name,
        type: 'Infrabel Moederbundel / Rangeerstation',
        cluster: 'bundel',
        zone: 'INFRABEL',
        zone_name: 'Infrabel Vormingsbundel',
        has_bi: false,
        moederbundel: 'Hoofdspoor Infrabel',
        sporen: b.info || 'Rangeersporen',
        adres: b.name + ', West-Vlaanderen',
        toegang_weg: 'Spoorwegtoegang Infrabel',
        beveiliging: 'Bediend seinwezen / Centrale Blokpost',
        ppgi_ref: 'PPGI West-Vlaanderen',
        original_lat: b.lat,
        original_lng: b.lng,
        lat: lat,
        lng: lng,
        aliases: [b.name],
        is_custom_coord: hasCustom,
        is_bundel: true
      }});
    }});

    // Add Markers to Map
    function buildMapMarkers() {{
      // Clear existing
      Object.values(markersMap).forEach(mObj => map.removeLayer(mObj.marker));
      markersMap = {{}};

      allItems.forEach(item => {{
        const marker = L.marker([item.lat, item.lng], {{
          icon: createMarkerIcon(item, item.is_custom_coord),
          riseOnHover: true
        }}).addTo(map);

        const tipText = item.is_bundel 
          ? `<strong>${{item.name}}</strong><br/><span style="color:#fbbf24;font-size:10px;">Infrabel Moederbundel</span>`
          : `<strong>${{item.name}}</strong><br/><span style="color:${{item.has_bi ? '#34d399' : '#f87171'}};font-size:10px;">${{item.has_bi ? '🟢 Reeds BI' : '🔴 Nog GEEN BI'}}</span>`;

        marker.bindTooltip(tipText, {{
          className: 'custom-tip',
          direction: 'top',
          offset: [0, -14],
          opacity: 0.95
        }});

        marker.on('click', () => {{
          selectLocation(item.id, true);
        }});

        markersMap[item.id] = {{ marker, data: item }};
      }});
    }}
    buildMapMarkers();

    // Update Modified Counter Badge in Header
    function updateCustomCountBadge() {{
      const saved = loadPersistedOverrides();
      const count = Object.keys(saved).length;
      const badge = document.getElementById('savedCountPill');
      const num = document.getElementById('savedCountNum');
      const modalCount = document.getElementById('modalCustomCount');

      if (modalCount) modalCount.textContent = count;
      if (num) num.textContent = count;

      if (badge) {{
        badge.style.display = count > 0 ? 'flex' : 'none';
      }}
    }}
    updateCustomCountBadge();

    // Render Sidebar List
    function renderList(items) {{
      const listEl = document.getElementById('locationsList');
      listEl.innerHTML = '';

      items.forEach(item => {{
        const card = document.createElement('div');
        card.className = `loc-card ${{item.id === activeMarkerId ? 'selected' : ''}}`;
        card.id = `card_${{item.id}}`;

        let badgeHtml = '';
        if (item.is_bundel) {{
          badgeHtml = '<span class="loc-status-badge badge-bundel">BUNDEL</span>';
        }} else if (item.has_bi) {{
          badgeHtml = '<span class="loc-status-badge badge-bi-yes">✓ BI OK</span>';
        }} else {{
          badgeHtml = '<span class="loc-status-badge badge-bi-no">! GEEN BI</span>';
        }}

        const customBadge = item.is_custom_coord 
          ? '<span class="badge-custom-coord" title="Handmatig aangepast">📍 Aangepast</span>' 
          : '';

        // Aliases rendering in card
        let aliasesHtml = '';
        if (item.aliases && item.aliases.length > 0) {{
          const displayed = item.aliases.slice(0, 3);
          aliasesHtml = `
            <div class="loc-card-aliases">
              <span>🔗</span>
              ${{displayed.map(a => `<span class="loc-card-aliases-tag">${{a}}</span>`).join('')}}
              ${{item.aliases.length > 3 ? `<span style="color:#64748b;">+${{item.aliases.length - 3}}</span>` : ''}}
            </div>
          `;
        }}

        card.innerHTML = `
          <div class="loc-card-header">
            <div class="loc-card-title">${{item.name}}</div>
            ${{badgeHtml}}
          </div>
          <div class="loc-card-details">
            <div>📍 ${{item.moederbundel || item.adres}}</div>
            <div style="color:#64748b; font-size:10px;">Sporen: ${{item.sporen}}</div>
            ${{aliasesHtml}}
          </div>
          <div class="loc-card-meta">
            <span>${{item.zone}}</span>
            <span>${{item.type}}</span>
            ${{customBadge}}
          </div>
        `;

        card.addEventListener('click', () => {{
          selectLocation(item.id, true);
        }});

        listEl.appendChild(card);
      }});

      // Update count statistics
      const biYesCount = allItems.filter(x => !x.is_bundel && x.has_bi).length;
      const biNoCount = allItems.filter(x => !x.is_bundel && !x.has_bi).length;
      const bundelCount = allItems.filter(x => x.is_bundel).length;

      document.getElementById('resultCount').textContent = `${{items.length}} locaties getoond`;
      document.getElementById('filterAll').textContent = `Alle (${{allItems.length}})`;
      document.getElementById('filterBiYes').textContent = `🟢 Reeds BI (${{biYesCount}})`;
      document.getElementById('filterBiNo').textContent = `🔴 Nog geen BI (${{biNoCount}})`;
      document.getElementById('filterBundels').textContent = `🟡 Bundels (${{bundelCount}})`;
      document.getElementById('legBiYesText').textContent = `Reeds een BI (${{biYesCount}} locaties)`;
      document.getElementById('legBiNoText').textContent = `Nog GEEN BI (${{biNoCount}} locaties)`;
    }}

    // Filter Logic
    function handleFilter() {{
      const query = document.getElementById('searchInput').value.toLowerCase().trim();

      const filtered = allItems.filter(item => {{
        if (currentFilter === 'bi-yes' && (!item.has_bi || item.is_bundel)) return false;
        if (currentFilter === 'bi-no' && (item.has_bi || item.is_bundel)) return false;
        if (currentFilter === 'bundel' && !item.is_bundel) return false;

        if (query) {{
          const matchName = item.name.toLowerCase().includes(query);
          const matchSporen = (item.sporen || '').toLowerCase().includes(query);
          const matchAdres = (item.adres || '').toLowerCase().includes(query);
          const matchZone = (item.zone || '').toLowerCase().includes(query);
          const matchMoeder = (item.moederbundel || '').toLowerCase().includes(query);
          const matchAlias = (item.aliases || []).some(a => a.toLowerCase().includes(query));
          if (!matchName && !matchSporen && !matchAdres && !matchZone && !matchMoeder && !matchAlias) return false;
        }}
        return true;
      }});

      allItems.forEach(item => {{
        if (!markersMap[item.id]) return;
        const m = markersMap[item.id].marker;
        const visible = filtered.some(f => f.id === item.id);
        if (visible) {{
          if (!map.hasLayer(m)) map.addLayer(m);
        }} else {{
          if (map.hasLayer(m)) map.removeLayer(m);
        }}
      }});

      renderList(filtered);
    }}

    function setFilter(type, btn) {{
      currentFilter = type;
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      handleFilter();
    }}

    // Selection & Detail Overlay
    function selectLocation(id, zoomIn) {{
      cancelInteractiveTool();

      activeMarkerId = id;
      const target = allItems.find(x => x.id === id);
      if (!target) return;

      document.querySelectorAll('.loc-card').forEach(c => c.classList.remove('selected'));
      const card = document.getElementById(`card_${{id}}`);
      if (card) {{
        card.classList.add('selected');
        card.scrollIntoView({{ behavior: 'smooth', block: 'nearest' }});
      }}

      if (zoomIn) {{
        map.flyTo([target.lat, target.lng], 16, {{
          duration: 1.0,
          easeLinearity: 0.25
        }});
      }}

      // Populate Detail Card
      const overlay = document.getElementById('detailOverlay');
      const pill = document.getElementById('detailStatusPill');

      if (target.is_bundel) {{
        pill.className = 'detail-status-pill badge-bundel';
        pill.textContent = '◆ INFRABEL MOEDERBUNDEL';
      }} else if (target.has_bi) {{
        pill.className = 'detail-status-pill badge-bi-yes';
        pill.textContent = `✓ BI BESCHIKBAAR (${{target.bi_version || 'Actief'}})`;
      }} else {{
        pill.className = 'detail-status-pill badge-bi-no';
        pill.textContent = '! NOG GEEN BI OPGESTELD';
      }}

      document.getElementById('detailTitle').textContent = target.name;
      document.getElementById('detailSubtitle').textContent = `${{target.zone_name}} • ${{target.zone}} • ${{target.type}}`;
      document.getElementById('detailMoederbundel').textContent = target.moederbundel || 'N.v.t.';
      document.getElementById('detailSporen').textContent = target.sporen || 'N.v.t.';
      document.getElementById('detailAdres').textContent = target.adres || 'N.v.t.';
      document.getElementById('detailBeveiliging').textContent = target.beveiliging || 'Geen specifieke sloten vermeld';
      document.getElementById('detailPpgi').textContent = target.ppgi_ref || 'PPGI West-Vlaanderen';

      // Render Aliases Section
      renderDetailAliases(target);

      // GPS Inputs
      document.getElementById('editLat').value = target.lat.toFixed(6);
      document.getElementById('editLng').value = target.lng.toFixed(6);
      document.getElementById('coordCustomBadge').style.display = target.is_custom_coord ? 'inline-block' : 'none';

      // Google maps link
      document.getElementById('detailNavBtn').href = `https://www.google.com/maps/@?api=1&map_action=map&center=${{target.lat}},${{target.lng}}&zoom=18&basemap=satellite`;

      overlay.classList.add('active');
    }}

    function closeDetail() {{
      cancelInteractiveTool();
      document.getElementById('detailOverlay').classList.remove('active');
      document.querySelectorAll('.loc-card').forEach(c => c.classList.remove('selected'));
      activeMarkerId = null;
    }}

    function toggleSidebar() {{
      const sidebar = document.getElementById('sidebar');
      sidebar.classList.toggle('collapsed');
      const isCollapsed = sidebar.classList.contains('collapsed');
      document.getElementById('toggleIcon').innerHTML = isCollapsed 
        ? '<polyline points="9 18 15 12 9 6"></polyline>' 
        : '<polyline points="15 18 9 12 15 6"></polyline>';
      setTimeout(() => map.invalidateSize(), 300);
    }}

    // ==========================================
    // ALIASES & LINKING LOGIC (TASK 2)
    // ==========================================

    function renderDetailAliases(target) {{
      const sec = document.getElementById('detailAliasSection');
      if (target.is_bundel) {{
        sec.style.display = 'none';
        return;
      }}
      sec.style.display = 'block';

      const countEl = document.getElementById('detailAliasCount');
      const container = document.getElementById('detailAliasesContainer');
      const selectEl = document.getElementById('mergeLocationSelect');

      const aliases = target.aliases || [];
      countEl.textContent = `${{aliases.length}} synoniem${{aliases.length === 1 ? '' : 'men'}}`;

      if (aliases.length === 0) {{
        container.innerHTML = '<span style="color:#64748b; font-size:11px; font-style:italic;">Nog geen synoniemen gekoppeld. Voeg er een toe om dubbele BI\\'s te voorkomen.</span>';
      }} else {{
        container.innerHTML = aliases.map(a => `
          <span class="alias-chip">
            <span>${{a}}</span>
            <button class="alias-chip-del" onclick="removeCurrentAlias('${{a.replace(/'/g, "\\\\'")}}')" title="Verwijder synoniem">&times;</button>
          </span>
        `).join('');
      }}

      // Populate merge dropdown with other non-bundel locations
      selectEl.innerHTML = '<option value="">-- Koppel met andere bediening --</option>';
      allItems.filter(x => !x.is_bundel && x.id !== target.id).forEach(other => {{
        const opt = document.createElement('option');
        opt.value = other.id;
        opt.textContent = `${{other.name}} (${{other.has_bi ? 'Reeds BI' : 'Geen BI'}})`;
        selectEl.appendChild(opt);
      }});
    }}

    function addCurrentAlias() {{
      if (!activeMarkerId) return;
      const target = allItems.find(x => x.id === activeMarkerId);
      if (!target) return;

      const input = document.getElementById('newAliasInput');
      const val = input.value.trim();
      if (!val) return;

      if (!target.aliases) target.aliases = [];
      if (!target.aliases.includes(val)) {{
        target.aliases.push(val);
        input.value = '';

        // Save aliases to localStorage
        const allStoredAliases = loadPersistedAliases();
        allStoredAliases[target.id] = target.aliases;
        savePersistedAliases(allStoredAliases);

        renderDetailAliases(target);
        handleFilter();
        showToast(`✓ Synoniem "${{val}}" gekoppeld aan ${{target.name}}!`);
      }}
    }}

    function removeCurrentAlias(aliasVal) {{
      if (!activeMarkerId) return;
      const target = allItems.find(x => x.id === activeMarkerId);
      if (!target || !target.aliases) return;

      target.aliases = target.aliases.filter(a => a !== aliasVal);

      const allStoredAliases = loadPersistedAliases();
      allStoredAliases[target.id] = target.aliases;
      savePersistedAliases(allStoredAliases);

      renderDetailAliases(target);
      handleFilter();
      showToast(`Synoniem "${{aliasVal}}" verwijderd.`);
    }}

    function mergeSelectedLocation() {{
      if (!activeMarkerId) return;
      const target = allItems.find(x => x.id === activeMarkerId);
      if (!target) return;

      const selectEl = document.getElementById('mergeLocationSelect');
      const otherId = selectEl.value;
      if (!otherId) {{
        showToast('Selecteer eerst een locatie om samen te voegen.', 'warning');
        return;
      }}

      const other = allItems.find(x => x.id === otherId);
      if (!other) return;

      const confirmMsg = `Weet je zeker dat je "${{other.name}}" wilt samenvoegen met "${{target.name}}"?\\n\\nBeide benamingen worden gekoppeld en vormen voortaan 1 GEZAMENLIJKE BI. De dubbele pin van "${{other.name}}" wordt verwijderd.`;
      if (!confirm(confirmMsg)) return;

      // Add other name and aliases to target
      if (!target.aliases) target.aliases = [];
      if (!target.aliases.includes(other.name)) target.aliases.push(other.name);
      if (other.aliases) {{
        other.aliases.forEach(a => {{
          if (!target.aliases.includes(a)) target.aliases.push(a);
        }});
      }}

      // If target had no BI but other had a BI, inherit the BI!
      if (!target.has_bi && other.has_bi) {{
        target.has_bi = true;
        target.bi_version = other.bi_version;
      }}

      // Remove other location from allItems
      allItems = allItems.filter(x => x.id !== otherId);

      // Save aliases and rebuild map markers
      const allStoredAliases = loadPersistedAliases();
      allStoredAliases[target.id] = target.aliases;
      savePersistedAliases(allStoredAliases);

      buildMapMarkers();
      selectLocation(target.id, false);
      handleFilter();

      showToast(`✓ "${{other.name}}" succesvol gekoppeld aan "${{target.name}}"! Slechts 1 BI vereist.`);
    }}

    // ==========================================
    // INTERACTIVE COORDINATES EDITING LOGIC
    // ==========================================

    function toggleDragCurrentMarker() {{
      if (!activeMarkerId) return;
      const itemObj = markersMap[activeMarkerId];
      if (!itemObj) return;
      const marker = itemObj.marker;

      isDraggingActive = !isDraggingActive;
      const btn = document.getElementById('btnDragMarker');
      const btnText = document.getElementById('btnDragText');
      const banner = document.getElementById('actionBanner');
      const bannerText = document.getElementById('actionBannerText');

      if (isDraggingActive) {{
        if (isPickPointActive) disablePickPoint();
        marker.dragging.enable();
        btn.classList.add('active');
        btnText.textContent = 'Verslepen Actief...';
        
        banner.classList.add('active');
        bannerText.innerHTML = `📍 <strong>${{itemObj.data.name}}</strong>: Sleep de marker naar de exacte positie op de satelliet en klik op <strong>'Positie Opslaan'</strong>.`;

        const el = marker.getElement();
        if (el) el.classList.add('is-being-dragged');

        marker.on('drag', onMarkerDrag);
        marker.on('dragend', onMarkerDragEnd);
      }} else {{
        disableDrag();
      }}
    }}

    function onMarkerDrag(e) {{
      const latlng = e.latlng;
      document.getElementById('editLat').value = latlng.lat.toFixed(6);
      document.getElementById('editLng').value = latlng.lng.toFixed(6);
    }}

    function onMarkerDragEnd(e) {{
      const latlng = e.target.getLatLng();
      document.getElementById('editLat').value = latlng.lat.toFixed(6);
      document.getElementById('editLng').value = latlng.lng.toFixed(6);
    }}

    function disableDrag() {{
      isDraggingActive = false;
      const btn = document.getElementById('btnDragMarker');
      const btnText = document.getElementById('btnDragText');
      if (btn) btn.classList.remove('active');
      if (btnText) btnText.textContent = 'Marker Verslepen';

      if (activeMarkerId && markersMap[activeMarkerId]) {{
        const marker = markersMap[activeMarkerId].marker;
        marker.dragging.disable();
        marker.off('drag', onMarkerDrag);
        marker.off('dragend', onMarkerDragEnd);
        const el = marker.getElement();
        if (el) el.classList.remove('is-being-dragged');
      }}
    }}

    function togglePickPoint() {{
      if (!activeMarkerId) return;
      isPickPointActive = !isPickPointActive;
      const btn = document.getElementById('btnPickPoint');
      const btnText = document.getElementById('btnPickText');
      const banner = document.getElementById('actionBanner');
      const bannerText = document.getElementById('actionBannerText');

      if (isPickPointActive) {{
        if (isDraggingActive) disableDrag();
        btn.classList.add('active');
        btnText.textContent = 'Prikken Actief...';
        document.getElementById('map').style.cursor = 'crosshair';

        const itemObj = markersMap[activeMarkerId];
        banner.classList.add('active');
        bannerText.innerHTML = `📍 Klik ergens op de satellietkaart om de nieuwe positie van <strong>${{itemObj.data.name}}</strong> vast te leggen.`;
      }} else {{
        disablePickPoint();
      }}
    }}

    function disablePickPoint() {{
      isPickPointActive = false;
      const btn = document.getElementById('btnPickPoint');
      const btnText = document.getElementById('btnPickText');
      if (btn) btn.classList.remove('active');
      if (btnText) btnText.textContent = 'Prikken op Kaart';
      document.getElementById('map').style.cursor = '';
    }}

    function cancelInteractiveTool() {{
      disableDrag();
      disablePickPoint();
      document.getElementById('actionBanner').classList.remove('active');
    }}

    map.on('click', function(e) {{
      if (isPickPointActive && activeMarkerId) {{
        const newLat = e.latlng.lat;
        const newLng = e.latlng.lng;
        document.getElementById('editLat').value = newLat.toFixed(6);
        document.getElementById('editLng').value = newLng.toFixed(6);

        const itemObj = markersMap[activeMarkerId];
        itemObj.marker.setLatLng([newLat, newLng]);

        disablePickPoint();
        showToast('📍 Positie geplaatst op kaart. Klik op "Positie Opslaan" om te bevestigen.');
      }}
    }});

    function onManualCoordInputChange() {{
      if (!activeMarkerId) return;
      const newLat = parseFloat(document.getElementById('editLat').value);
      const newLng = parseFloat(document.getElementById('editLng').value);
      if (!isNaN(newLat) && !isNaN(newLng)) {{
        const itemObj = markersMap[activeMarkerId];
        itemObj.marker.setLatLng([newLat, newLng]);
      }}
    }}

    async function saveCurrentCoords() {{
      if (!activeMarkerId) return;
      const newLat = parseFloat(document.getElementById('editLat').value);
      const newLng = parseFloat(document.getElementById('editLng').value);

      if (isNaN(newLat) || isNaN(newLng) || newLat < 49.0 || newLat > 52.0 || newLng < 2.0 || newLng > 7.0) {{
        showToast('Ongeldige GPS coördinaten voor België (Lat: 49-52, Lng: 2-7)', 'warning');
        return;
      }}

      cancelInteractiveTool();

      const itemObj = markersMap[activeMarkerId];
      const target = itemObj.data;
      target.lat = newLat;
      target.lng = newLng;
      target.is_custom_coord = true;

      itemObj.marker.setLatLng([newLat, newLng]);
      itemObj.marker.setIcon(createMarkerIcon(target, true));

      const saved = loadPersistedOverrides();
      saved[activeMarkerId] = {{ lat: newLat, lng: newLng }};
      savePersistedOverrides(saved);

      document.getElementById('coordCustomBadge').style.display = 'inline-block';
      document.getElementById('detailNavBtn').href = `https://www.google.com/maps/@?api=1&map_action=map&center=${{newLat}},${{newLng}}&zoom=18&basemap=satellite`;

      handleFilter();

      let serverSaved = false;
      if (serverAvailable) {{
        try {{
          const res = await fetch('http://localhost:8055/api/save', {{
            method: 'POST',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ id: activeMarkerId, lat: newLat, lng: newLng }})
          }});
          if (res.ok) serverSaved = true;
        }} catch (e) {{}}
      }}

      if (serverSaved) {{
        showToast(`✓ Positie voor ${{target.name}} opgeslagen in bestand & browser!`);
      }} else {{
        showToast(`✓ Positie voor ${{target.name}} bewaard in browser (LocalStorage)!`);
      }}
    }}

    function resetCurrentCoords() {{
      if (!activeMarkerId) return;
      const itemObj = markersMap[activeMarkerId];
      const target = itemObj.data;

      cancelInteractiveTool();

      target.lat = target.original_lat;
      target.lng = target.original_lng;
      target.is_custom_coord = false;

      itemObj.marker.setLatLng([target.lat, target.lng]);
      itemObj.marker.setIcon(createMarkerIcon(target, false));

      document.getElementById('editLat').value = target.lat.toFixed(6);
      document.getElementById('editLng').value = target.lng.toFixed(6);
      document.getElementById('coordCustomBadge').style.display = 'none';

      const saved = loadPersistedOverrides();
      delete saved[activeMarkerId];
      savePersistedOverrides(saved);

      handleFilter();
      showToast(`Positie hersteld naar origineel voor ${{target.name}}`);
    }}

    // ==========================================
    // EXPORT & MODAL LOGIC
    // ==========================================

    function openExportModal() {{
      updateCustomCountBadge();
      document.getElementById('exportModal').classList.add('active');
    }}

    function closeExportModal() {{
      document.getElementById('exportModal').classList.remove('active');
    }}

    function downloadUpdatedJson() {{
      const updatedLocations = allItems.filter(x => !x.is_bundel).map(item => {{
        return {{
          id: item.id,
          name: item.name,
          cluster: item.cluster,
          zone: item.zone,
          zone_name: item.zone_name,
          has_bi: item.has_bi,
          bi_version: item.bi_version,
          type: item.type,
          moederbundel: item.moederbundel,
          sporen: item.sporen,
          adres: item.adres,
          toegang_weg: item.toegang_weg,
          beveiliging: item.beveiliging,
          ppgi_ref: item.ppgi_ref,
          aliases: item.aliases || [],
          lat: item.lat,
          lng: item.lng
        }};
      }});

      const updatedBundels = rawBundels.map((b, idx) => {{
        const item = allItems.find(x => x.id === 'bundel_' + idx);
        return {{
          ...b,
          lat: item ? item.lat : b.lat,
          lng: item ? item.lng : b.lng
        }};
      }});

      const fullJson = {{
        locations: updatedLocations,
        bundels: updatedBundels
      }};

      const blob = new Blob([JSON.stringify(fullJson, null, 2)], {{ type: 'application/json' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'locs_gps.json';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast('📥 locs_gps.json succesvol gedownload!');
    }}

    function downloadUpdatedHtml() {{
      let html = document.documentElement.outerHTML;
      const blob = new Blob(['<!DOCTYPE html>' + String.fromCharCode(10) + html], {{ type: 'text/html' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'kaart_bedieningen.html';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showToast('📄 Bijgewerkte kaart_bedieningen.html gedownload!');
    }}

    function copyModifiedCoordsToClipboard() {{
      const saved = loadPersistedOverrides();
      const keys = Object.keys(saved);
      if (keys.length === 0) {{
        showToast('Er zijn nog geen gewijzigde coördinaten om te kopiëren.', 'warning');
        return;
      }}

      let text = 'DB Cargo Belgium - Gewijzigde GPS Coördinaten:\\n\\n';
      keys.forEach(k => {{
        const item = allItems.find(x => x.id === k);
        const name = item ? item.name : k;
        text += `${{name}} [${{k}}]: Lat: ${{saved[k].lat.toFixed(6)}}, Lng: ${{saved[k].lng.toFixed(6)}}\\n`;
      }});

      navigator.clipboard.writeText(text).then(() => {{
        showToast('📋 Gewijzigde coördinaten gekopieerd naar klembord!');
      }}).catch(() => {{
        showToast('Kopiëren niet toegestaan door browserbeveiliging.', 'warning');
      }});
    }}

    function resetAllOverrides() {{
      if (confirm('Weet je zeker dat je alle handmatige aanpassingen wilt wissen en terugkeren naar de fabrieksinstellingen?')) {{
        localStorage.removeItem(STORAGE_KEY);
        localStorage.removeItem(STORAGE_ALIASES_KEY);
        allItems.forEach(item => {{
          item.lat = item.original_lat;
          item.lng = item.original_lng;
          item.is_custom_coord = false;
          const m = markersMap[item.id].marker;
          m.setLatLng([item.lat, item.lng]);
          m.setIcon(createMarkerIcon(item, false));
        }});
        updateCustomCountBadge();
        handleFilter();
        closeExportModal();
        if (activeMarkerId) selectLocation(activeMarkerId, false);
        showToast('Alle aanpassingen gewist. Fabrieksinstellingen hersteld.');
      }}
    }}

    // Initialize
    renderList(allItems);
    checkServerStatus();
  </script>
</body>
</html>
'''

if __name__ == '__main__':
    workspace_dir = r'd:\Users\BKU\BartVercaempst\OneDrive - Deutsche Bahn\Documents\26-AI-Projecten\BI Generator'
    json_path = os.path.join(workspace_dir, 'locs_gps.json')
    if not os.path.exists(json_path):
        json_path = os.path.expandvars('%TEMP%\\locs_gps.json')
    
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    
    html = build_map_html(data['locations'], data.get('bundels', []))
    
    # Save to workspace (both kaart_bedieningen.html and index.html for GitHub Pages)
    ws_html = os.path.join(workspace_dir, 'kaart_bedieningen.html')
    with open(ws_html, 'w', encoding='utf-8') as f:
        f.write(html)

    ws_index = os.path.join(workspace_dir, 'index.html')
    with open(ws_index, 'w', encoding='utf-8') as f:
        f.write(html)
        
    # Save to artifact directory
    artifact_dir = r'C:\Users\bartvercaempst\.gemini\antigravity\brain\ef3e86e7-5525-45fe-83e0-530122591b51'
    art_html = os.path.join(artifact_dir, 'kaart_bedieningen.html')
    with open(art_html, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Generated successfully: written to {ws_html}, {ws_index} and {art_html}")
