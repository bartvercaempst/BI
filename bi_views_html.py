"""
HTML, CSS and JS view components for:
- 📄 BI Generator & PDF Export (with 5-level breadcrumbs, uniform 8-chapter preview, changelog versioning)
- 🔍 PPGI Vergelijker & Audit Voorstellen (with diff comparisons and interactive 'Pas toe' actions)
- Master data inspection modal for cascading levels 1-4
"""

import json

def get_bi_styles():
    return '''
    /* ======================================================== */
    /* TOP NAVIGATION TABS                                      */
    /* ======================================================== */
    .header-main-tabs {
      display: flex;
      align-items: center;
      gap: 6px;
      margin-left: 12px;
      margin-right: 12px;
      flex-shrink: 0;
    }
    .nav-tab-btn {
      background: #1e293b;
      color: #94a3b8;
      border: 1px solid #334155;
      padding: 0 14px;
      height: 36px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .nav-tab-btn:hover {
      background: #334155;
      color: #f8fafc;
      border-color: #475569;
    }
    .nav-tab-btn.active {
      background: #2563eb;
      color: #ffffff;
      border-color: #3b82f6;
      box-shadow: 0 0 12px rgba(37, 99, 235, 0.45);
    }
    .nav-tab-btn .tab-badge {
      background: #ef4444;
      color: white;
      font-size: 10px;
      font-weight: 800;
      padding: 2px 6px;
      border-radius: 10px;
      line-height: 1;
    }
    .nav-tab-btn.active .tab-badge {
      background: #ffffff;
      color: #2563eb;
    }

    /* Mobile Drawer Tab buttons */
    .drawer-view-selector {
      display: flex;
      flex-direction: column;
      gap: 8px;
      margin-bottom: 14px;
    }
    .drawer-tab-btn {
      background: #1e293b;
      color: #cbd5e1;
      border: 1px solid #334155;
      padding: 12px 14px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 700;
      text-align: left;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.15s ease;
    }
    .drawer-tab-btn:hover {
      background: #334155;
      color: #ffffff;
    }
    .drawer-tab-btn.active {
      background: #2563eb;
      color: #ffffff;
      border-color: #3b82f6;
    }

    /* ======================================================== */
    /* VIEW CONTAINERS                                          */
    /* ======================================================== */
    #mapView {
      width: 100%;
      height: 100%;
      display: flex;
      position: relative;
      overflow: hidden;
      flex: 1;
    }
    #biGeneratorView, #ppgiReviewView {
      width: 100%;
      height: 100%;
      display: none;
      flex-direction: column;
      overflow-y: auto;
      background: #0b1120;
      color: #f1f5f9;
      padding: 20px 24px;
      box-sizing: border-box;
      flex: 1;
    }

    /* ======================================================== */
    /* BI GENERATOR VIEW STYLES                                 */
    /* ======================================================== */
    .bi-top-toolbar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      background: #1e293b;
      border: 1px solid #334155;
      padding: 14px 18px;
      border-radius: 12px;
      margin-bottom: 18px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    }
    .bi-selector-group {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      flex: 1;
    }
    .bi-selector-label {
      font-size: 13px;
      font-weight: 800;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .bi-select-dropdown {
      background: #0f172a;
      border: 1px solid #475569;
      color: #f8fafc;
      padding: 9px 14px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 700;
      outline: none;
      cursor: pointer;
      min-width: 280px;
      max-width: 100%;
      transition: border-color 0.2s;
    }
    .bi-select-dropdown:focus {
      border-color: #38bdf8;
      box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25);
    }

    .bi-toolbar-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .btn-bi-primary {
      background: #2563eb;
      color: #ffffff;
      border: 1px solid #3b82f6;
      padding: 9px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      transition: all 0.2s;
      box-shadow: 0 2px 8px rgba(37, 99, 235, 0.35);
    }
    .btn-bi-primary:hover {
      background: #1d4ed8;
      transform: translateY(-1px);
    }
    .btn-bi-success {
      background: #059669;
      color: #ffffff;
      border: 1px solid #10b981;
      padding: 9px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      transition: all 0.2s;
      box-shadow: 0 2px 8px rgba(16, 185, 129, 0.35);
    }
    .btn-bi-success:hover {
      background: #047857;
      transform: translateY(-1px);
    }
    .btn-bi-secondary {
      background: #334155;
      color: #e2e8f0;
      border: 1px solid #475569;
      padding: 9px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-bi-secondary:hover {
      background: #475569;
      color: #ffffff;
    }

    /* 5-Level Cascading Hierarchy Breadcrumbs */
    .bi-breadcrumbs-wrap {
      background: #131d31;
      border: 1px solid #1e293b;
      padding: 14px 18px;
      border-radius: 12px;
      margin-bottom: 20px;
    }
    .bi-breadcrumbs-title {
      font-size: 11px;
      font-weight: 800;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .bi-breadcrumbs-list {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }
    .bi-crumb-card {
      background: #1e293b;
      border: 1px solid #334155;
      padding: 8px 12px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .bi-crumb-card:hover {
      border-color: #38bdf8;
      background: #243247;
      transform: translateY(-1px);
    }
    .bi-crumb-level {
      font-size: 10px;
      font-weight: 800;
      color: #38bdf8;
      text-transform: uppercase;
    }
    .bi-crumb-name {
      font-size: 13px;
      font-weight: 700;
      color: #f8fafc;
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .bi-crumb-arrow {
      color: #64748b;
      font-weight: 800;
      font-size: 16px;
    }

    /* Document Sheet Preview Card */
    .bi-doc-card {
      background: #0f172a;
      border: 1px solid #334155;
      border-radius: 12px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
      margin-bottom: 30px;
      overflow: hidden;
    }
    .bi-doc-header-banner {
      background: linear-gradient(135deg, #1e293b 0%, #090d16 100%);
      border-bottom: 3px solid #2563eb;
      padding: 24px 30px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      flex-wrap: wrap;
    }
    .bi-doc-branding {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .bi-doc-logo {
      background: #dc2626;
      color: #ffffff;
      font-size: 18px;
      font-weight: 900;
      padding: 8px 14px;
      border-radius: 6px;
      letter-spacing: 0.5px;
    }
    .bi-doc-title-box h1 {
      font-size: 22px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.2;
      margin-bottom: 4px;
    }
    .bi-doc-title-box p {
      font-size: 13px;
      color: #94a3b8;
    }
    .bi-doc-version-pill {
      background: rgba(37, 99, 235, 0.18);
      border: 1px solid #3b82f6;
      color: #93c5fd;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 800;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }

    /* Metadata Grid */
    .bi-meta-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 12px;
      background: #131c2e;
      border-bottom: 1px solid #1e293b;
      padding: 16px 30px;
    }
    .bi-meta-cell {
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .bi-meta-label {
      font-size: 11px;
      font-weight: 800;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .bi-meta-val {
      font-size: 13px;
      font-weight: 700;
      color: #e2e8f0;
    }

    /* Chapters Content */
    .bi-doc-body {
      padding: 24px 30px;
      display: flex;
      flex-direction: column;
      gap: 28px;
    }
    .bi-chapter {
      border: 1px solid #1e293b;
      border-radius: 10px;
      overflow: hidden;
      background: rgba(15, 23, 42, 0.5);
    }
    .bi-chapter-title {
      background: #1e293b;
      border-bottom: 1px solid #334155;
      padding: 12px 18px;
      font-size: 15px;
      font-weight: 800;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .bi-chapter-content {
      padding: 16px 20px;
      font-size: 13px;
      line-height: 1.6;
      color: #cbd5e1;
    }

    /* Tables in Document */
    .bi-table {
      width: 100%;
      border-collapse: collapse;
      margin: 10px 0;
      font-size: 13px;
    }
    .bi-table th {
      background: #1e293b;
      color: #94a3b8;
      font-weight: 800;
      text-align: left;
      padding: 9px 12px;
      border-bottom: 1px solid #334155;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .bi-table td {
      padding: 9px 12px;
      border-bottom: 1px solid #1e293b;
      color: #e2e8f0;
      vertical-align: middle;
    }
    .bi-table tr:hover td {
      background: rgba(51, 65, 85, 0.3);
    }
    .badge-level {
      display: inline-block;
      font-size: 10px;
      font-weight: 800;
      padding: 2px 7px;
      border-radius: 4px;
      letter-spacing: 0.4px;
    }
    .badge-level-1 { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4); }
    .badge-level-2 { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4); }
    .badge-level-3 { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }
    .badge-level-4 { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); }
    .badge-level-5 { background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }

    /* Steps list */
    .bi-step-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin: 10px 0;
    }
    .bi-step-item {
      display: flex;
      align-items: flex-start;
      gap: 14px;
      background: #131d31;
      border: 1px solid #1e293b;
      padding: 12px 16px;
      border-radius: 8px;
    }
    .bi-step-num {
      background: #2563eb;
      color: #ffffff;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      font-weight: 800;
      font-size: 13px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      margin-top: 1px;
    }
    .bi-step-text strong {
      display: block;
      color: #f8fafc;
      font-size: 14px;
      margin-bottom: 2px;
    }
    .bi-step-text p {
      margin: 0;
      color: #cbd5e1;
      font-size: 13px;
    }

    /* Warning callout box */
    .bi-callout-warning {
      background: rgba(245, 158, 11, 0.1);
      border-left: 4px solid #f59e0b;
      padding: 12px 16px;
      border-radius: 0 8px 8px 0;
      margin: 10px 0;
      color: #fef3c7;
      font-size: 13px;
    }
    .bi-callout-danger {
      background: rgba(239, 68, 68, 0.1);
      border-left: 4px solid #ef4444;
      padding: 12px 16px;
      border-radius: 0 8px 8px 0;
      margin: 10px 0;
      color: #fee2e2;
      font-size: 13px;
    }

    /* ======================================================== */
    /* PPGI REVIEWER VIEW STYLES                                */
    /* ======================================================== */
    .ppgi-audit-banner {
      background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
      border: 1px solid #334155;
      border-radius: 12px;
      padding: 20px 24px;
      margin-bottom: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }
    .ppgi-banner-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }
    .ppgi-banner-title h2 {
      font-size: 20px;
      font-weight: 800;
      color: #f8fafc;
      margin-bottom: 4px;
    }
    .ppgi-banner-title p {
      font-size: 13px;
      color: #94a3b8;
    }
    .ppgi-metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 12px;
    }
    .ppgi-metric-card {
      background: #131c2e;
      border: 1px solid #1e293b;
      padding: 12px 16px;
      border-radius: 8px;
      text-align: center;
    }
    .ppgi-metric-val {
      font-size: 24px;
      font-weight: 900;
      color: #f8fafc;
    }
    .ppgi-metric-label {
      font-size: 11px;
      font-weight: 700;
      color: #64748b;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .ppgi-proposals-list {
      display: flex;
      flex-direction: column;
      gap: 18px;
    }
    .ppgi-proposal-card {
      background: #131d31;
      border: 1px solid #334155;
      border-radius: 12px;
      overflow: hidden;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.2);
      transition: all 0.2s;
    }
    .ppgi-proposal-card.urgency-danger {
      border-left: 5px solid #ef4444;
    }
    .ppgi-proposal-card.urgency-warning {
      border-left: 5px solid #f59e0b;
    }
    .ppgi-proposal-card.urgency-info {
      border-left: 5px solid #38bdf8;
    }
    .ppgi-card-header {
      background: #1e293b;
      padding: 14px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      border-bottom: 1px solid #334155;
    }
    .ppgi-card-title-group {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .ppgi-prop-id {
      background: #0f172a;
      border: 1px solid #475569;
      color: #38bdf8;
      font-family: monospace !important;
      font-size: 12px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
    }
    .ppgi-prop-title {
      font-size: 15px;
      font-weight: 800;
      color: #f8fafc;
    }
    .badge-urgency {
      font-size: 11px;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 20px;
      letter-spacing: 0.5px;
    }
    .badge-urgency-danger { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }
    .badge-urgency-warning { background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }
    .badge-urgency-info { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid #38bdf8; }

    .ppgi-card-body {
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .ppgi-ref-badge-row {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      font-size: 12px;
      color: #94a3b8;
    }
    .ppgi-ref-tag {
      background: #1e293b;
      padding: 3px 8px;
      border-radius: 4px;
      border: 1px solid #334155;
      font-weight: 700;
      color: #e2e8f0;
    }

    /* Comparison diff box */
    .ppgi-diff-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    @media (max-width: 768px) {
      .ppgi-diff-grid {
        grid-template-columns: 1fr;
      }
    }
    .ppgi-diff-box {
      border-radius: 8px;
      padding: 12px 14px;
      font-size: 13px;
      line-height: 1.5;
    }
    .ppgi-diff-current {
      background: rgba(239, 68, 68, 0.08);
      border: 1px solid rgba(239, 68, 68, 0.3);
      color: #fca5a5;
    }
    .ppgi-diff-proposed {
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #86efac;
    }
    .ppgi-diff-label {
      font-size: 11px;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .ppgi-diff-current .ppgi-diff-label { color: #f87171; }
    .ppgi-diff-proposed .ppgi-diff-label { color: #34d399; }

    .ppgi-rationale-box {
      background: #1e293b;
      border-left: 3px solid #38bdf8;
      padding: 10px 14px;
      border-radius: 0 6px 6px 0;
      font-size: 12px;
      color: #cbd5e1;
      line-height: 1.5;
    }

    .ppgi-card-footer {
      background: #182234;
      border-top: 1px solid #243247;
      padding: 12px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }
    .btn-ppgi-apply {
      background: #2563eb;
      color: #ffffff;
      border: 1px solid #3b82f6;
      padding: 8px 16px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .btn-ppgi-apply:hover {
      background: #1d4ed8;
    }
    .btn-ppgi-applied {
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid #10b981;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 800;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      cursor: default;
    }

    /* ======================================================== */
    /* PRINT / PDF GENERATION STYLES                            */
    /* ======================================================== */
    @media print {
      @page {
        size: A4 portrait;
        margin: 12mm 15mm;
      }
      body {
        background: #ffffff !important;
        color: #111827 !important;
        font-size: 11pt !important;
        overflow: visible !important;
      }
      header, .mobile-hub-bar, .mobile-menu-drawer, .mobile-drawer-backdrop,
      .mobile-nav-pill, .modal-backdrop, #mapView, #ppgiReviewView,
      .bi-top-toolbar, .bi-breadcrumbs-wrap, .btn-coord-tool, .sidebar-toggle {
        display: none !important;
      }
      #biGeneratorView {
        display: block !important;
        padding: 0 !important;
        background: #ffffff !important;
        color: #111827 !important;
        overflow: visible !important;
        height: auto !important;
      }
      .bi-doc-card {
        border: none !important;
        box-shadow: none !important;
        background: #ffffff !important;
        color: #111827 !important;
        margin: 0 !important;
      }
      .bi-doc-header-banner {
        background: #ffffff !important;
        border-bottom: 2pt solid #dc2626 !important;
        padding: 10px 0 !important;
        color: #111827 !important;
      }
      .bi-doc-title-box h1 {
        color: #111827 !important;
        font-size: 16pt !important;
      }
      .bi-doc-title-box p {
        color: #4b5563 !important;
      }
      .bi-doc-version-pill {
        border: 1pt solid #111827 !important;
        color: #111827 !important;
        background: #f3f4f6 !important;
      }
      .bi-meta-grid {
        background: #f9fafb !important;
        border: 1pt solid #e5e7eb !important;
        color: #111827 !important;
        padding: 10px !important;
      }
      .bi-meta-val {
        color: #111827 !important;
      }
      .bi-chapter {
        background: #ffffff !important;
        border: 1pt solid #d1d5db !important;
        page-break-inside: avoid;
        margin-bottom: 14pt !important;
      }
      .bi-chapter-title {
        background: #f3f4f6 !important;
        color: #111827 !important;
        border-bottom: 1pt solid #d1d5db !important;
        font-size: 12pt !important;
      }
      .bi-chapter-content {
        color: #1f2937 !important;
        font-size: 10pt !important;
      }
      .bi-table {
        border: 1pt solid #9ca3af !important;
      }
      .bi-table th {
        background: #f3f4f6 !important;
        color: #111827 !important;
        border: 1pt solid #9ca3af !important;
      }
      .bi-table td {
        border: 1pt solid #e5e7eb !important;
        color: #111827 !important;
      }
      .bi-step-item {
        background: #f9fafb !important;
        border: 1pt solid #e5e7eb !important;
        color: #111827 !important;
        page-break-inside: avoid;
      }
      .bi-step-num {
        background: #111827 !important;
        color: #ffffff !important;
      }
      .bi-step-text strong {
        color: #111827 !important;
      }
      .bi-step-text p {
        color: #374151 !important;
      }
      .bi-callout-warning, .bi-callout-danger {
        background: #fef3c7 !important;
        color: #92400e !important;
        border: 1pt solid #f59e0b !important;
      }
    }
'''

def get_bi_html_markup(locations):
    # Sort locations with detailed ones first
    return f'''
    <!-- VIEW 2: BI GENERATOR & PDF EXPORT -->
    <div id="biGeneratorView">
      
      <!-- Top Action Toolbar -->
      <div class="bi-top-toolbar">
        <div class="bi-selector-group">
          <label class="bi-selector-label" for="biTerminalSelect">📄 Selecteer Bediening:</label>
          <select id="biTerminalSelect" class="bi-select-dropdown" onchange="onBiTerminalSelected(this.value)">
            <!-- Populated via JS -->
          </select>
        </div>

        <div class="bi-toolbar-actions">
          <button class="btn-bi-secondary" onclick="openMasterDataModal()" title="Bekijk gedeelde brongegevens Niveau 1 t/m 4">
            <span>🏢</span> Brongegevens
          </button>
          <button class="btn-bi-primary" onclick="openNewVersionModal()" title="Genereer een nieuwe versie van deze BI met geregistreerde wijzigingen">
            <span>➕</span> Nieuwe Versie Genereren
          </button>
          <button class="btn-bi-success" onclick="printBiDocument()" title="Exporteer als officiële PDF of print het document">
            <span>🖨️</span> Genereer PDF / Afdrukken
          </button>
        </div>
      </div>

      <!-- 5-Level Cascading Hierarchy Breadcrumbs -->
      <div class="bi-breadcrumbs-wrap">
        <div class="bi-breadcrumbs-title">
          <span>🏛️ Gelaagde Hiërarchie (Brongegevens Cascadering)</span>
          <span style="font-size: 11px; color: #38bdf8; font-weight: 600;">Klik op een niveau om gedeelde gegevens te inspecteren</span>
        </div>
        <div class="bi-breadcrumbs-list" id="biBreadcrumbsContainer">
          <!-- Rendered via JS -->
        </div>
      </div>

      <!-- Rendered BI Document Preview -->
      <div class="bi-doc-card" id="biDocumentCard">
        <!-- Rendered via renderBiDocument(terminalId) -->
      </div>
    </div>

    <!-- VIEW 3: PPGI VERGELIJKER & AUDIT VOORSTELLEN -->
    <div id="ppgiReviewView">
      
      <!-- Audit Header Banner -->
      <div class="ppgi-audit-banner">
        <div class="ppgi-banner-header">
          <div class="ppgi-banner-title">
            <h2>🔍 Infrabel PPGI Vergelijker & Audit Voorstellen</h2>
            <p>Geautomatiseerde audit die de recentste Bedieningsinstructies toetst aan de meest actuele Infrabel Plaatselijke Protocollen (PPGI)</p>
          </div>
          <button class="btn-bi-primary" onclick="switchMainTab('bi')">
            <span>📄</span> Naar BI Generator
          </button>
        </div>

        <div class="ppgi-metrics-grid">
          <div class="ppgi-metric-card">
            <div class="ppgi-metric-val" id="ppgiMetricTotal">5</div>
            <div class="ppgi-metric-label">Audit Voorstellen</div>
          </div>
          <div class="ppgi-metric-card">
            <div class="ppgi-metric-val" style="color: #ef4444;" id="ppgiMetricHigh">2</div>
            <div class="ppgi-metric-label">Hoge Urgentie</div>
          </div>
          <div class="ppgi-metric-card">
            <div class="ppgi-metric-val" style="color: #f59e0b;" id="ppgiMetricMedium">2</div>
            <div class="ppgi-metric-label">Medium Urgentie</div>
          </div>
          <div class="ppgi-metric-card">
            <div class="ppgi-metric-val" style="color: #10b981;" id="ppgiMetricApplied">0</div>
            <div class="ppgi-metric-label">Toegepast in BI</div>
          </div>
        </div>
      </div>

      <!-- Proposals List -->
      <div class="ppgi-proposals-list" id="ppgiProposalsContainer">
        <!-- Rendered via JS -->
      </div>
    </div>

    <!-- MODAL: NIEUWE VERSIE GENEREREN MET CHANGELOG -->
    <div class="modal-backdrop" id="newVersionModal">
      <div class="modal-box" style="width: 580px;">
        <h2>
          <span>➕ Nieuwe Versie BI Genereren</span>
          <button class="modal-close" onclick="closeNewVersionModal()">&times;</button>
        </h2>
        <div class="modal-body">
          <p id="newVersionModalIntro">Genereer een nieuwe officiële versie van de Bedieningsinstructie. Alle wijzigingen worden vastgelegd in het historische wijzigingenlogboek (Hoofdstuk 8).</p>
          
          <div class="modal-input-group" style="margin-top: 14px;">
            <label>Nieuw Versienummer</label>
            <input type="text" id="newVersionNumberInput" placeholder="bijv. 2.3" spellcheck="false" />
          </div>

          <div class="modal-input-group">
            <label>Versiedatum</label>
            <input type="date" id="newVersionDateInput" />
          </div>

          <div class="modal-input-group">
            <label>Auteur / Opsteller</label>
            <input type="text" id="newVersionAuthorInput" value="Bart VERCAEMPST Teamleader DBC.BE" spellcheck="false" />
          </div>

          <div class="modal-input-group">
            <label>Omschrijving van Wijzigingen (Changelog)</label>
            <textarea id="newVersionChangelogInput" rows="4" style="background:#090d16; border:1px solid #334155; color:#f1f5f9; padding:10px 12px; border-radius:6px; font-size:13px; outline:none; resize:vertical;" placeholder="Lijst alle doorgevoerde aanpassingen op (bijv. Aanpassing na PPGI audit v37.0: strikte 3-fasen procedure ingevoerd, mailbox seinhuis bijgewerkt)..."></textarea>
          </div>
        </div>
        <div class="modal-actions">
          <button class="btn-modal-action btn-modal-primary" onclick="submitNewBiVersion()">
            💾 Versie Vastleggen & Document Genereren
          </button>
          <button class="btn-modal-action" onclick="closeNewVersionModal()">
            Annuleren
          </button>
        </div>
      </div>
    </div>

    <!-- MODAL: BRONGEGEVENS INSPECTIE (NIVEAU 1 T/M 4) -->
    <div class="modal-backdrop" id="masterDataModal">
      <div class="modal-box" style="width: 680px; max-width: 95vw;">
        <h2>
          <span id="masterDataModalTitle">🏢 Gedeelde Brongegevens Inspecteren</span>
          <button class="modal-close" onclick="closeMasterDataModal()">&times;</button>
        </h2>
        <div class="modal-body" id="masterDataModalBody" style="max-height: 65vh; overflow-y: auto;">
          <!-- Dynamically filled -->
        </div>
        <div class="modal-actions">
          <button class="btn-modal-action" onclick="closeMasterDataModal()">
            Sluiten
          </button>
        </div>
      </div>
    </div>
    '''

def get_bi_javascript():
    return '''
    // ========================================================
    // BI GENERATOR & PPGI REVIEW JAVASCRIPT ENGINE
    // ========================================================

    const STORAGE_CUSTOM_BI_VERSIONS_KEY = 'db_cargo_bi_versions_v1';
    const STORAGE_APPLIED_PROPOSALS_KEY = 'db_cargo_applied_proposals_v1';

    let currentMainTab = 'map'; // 'map', 'bi', 'ppgi'
    let currentSelectedBiTerminalId = 'cro_brit';
    let biDataResolvedCache = {};
    let customVersionsStore = {};
    let appliedProposalsStore = {};

    // Initialize custom stores from localStorage
    try {
      const vRaw = localStorage.getItem(STORAGE_CUSTOM_BI_VERSIONS_KEY);
      if (vRaw) customVersionsStore = JSON.parse(vRaw);
    } catch(e) { console.error('Error loading custom versions', e); }

    try {
      const pRaw = localStorage.getItem(STORAGE_APPLIED_PROPOSALS_KEY);
      if (pRaw) appliedProposalsStore = JSON.parse(pRaw);
    } catch(e) { console.error('Error loading applied proposals', e); }

    // Tab Switcher
    function switchMainTab(tab) {
      currentMainTab = tab;

      // Update Nav Buttons
      const tabBtnMap = document.getElementById('tabBtnMap');
      const tabBtnBi = document.getElementById('tabBtnBi');
      const tabBtnPpgi = document.getElementById('tabBtnPpgi');
      if (tabBtnMap) tabBtnMap.classList.toggle('active', tab === 'map');
      if (tabBtnBi) tabBtnBi.classList.toggle('active', tab === 'bi');
      if (tabBtnPpgi) tabBtnPpgi.classList.toggle('active', tab === 'ppgi');

      // Update Drawer Tab Buttons
      const mobTabMap = document.getElementById('mobTabMap');
      const mobTabBi = document.getElementById('mobTabBi');
      const mobTabPpgi = document.getElementById('mobTabPpgi');
      if (mobTabMap) mobTabMap.classList.toggle('active', tab === 'map');
      if (mobTabBi) mobTabBi.classList.toggle('active', tab === 'bi');
      if (mobTabPpgi) mobTabPpgi.classList.toggle('active', tab === 'ppgi');

      // Toggle Views
      const mapView = document.getElementById('mapView');
      const biView = document.getElementById('biGeneratorView');
      const ppgiView = document.getElementById('ppgiReviewView');

      if (mapView) mapView.style.display = (tab === 'map') ? 'flex' : 'none';
      if (biView) biView.style.display = (tab === 'bi') ? 'flex' : 'none';
      if (ppgiView) ppgiView.style.display = (tab === 'ppgi') ? 'flex' : 'none';

      // Header controls visibility: Hub buttons and Map actions only on map
      const headerCenter = document.querySelector('.header-center');
      const headerRight = document.querySelector('.header-right');
      if (headerCenter && window.innerWidth > 900) {
        headerCenter.style.display = (tab === 'map') ? 'flex' : 'none';
      }

      if (tab === 'map') {
        setTimeout(() => { if (typeof map !== 'undefined') map.invalidateSize(); }, 150);
      } else if (tab === 'bi') {
        populateBiSelectDropdown();
        renderBiDocument(currentSelectedBiTerminalId);
      } else if (tab === 'ppgi') {
        renderPpgiProposals();
      }
    }

    // Populate Terminal Dropdown
    function populateBiSelectDropdown() {
      const select = document.getElementById('biTerminalSelect');
      if (!select || select.children.length > 0) return;

      const groupDetailed = document.createElement('optgroup');
      groupDetailed.label = "⭐ Gedetailleerde Bedieningsinstructies (Recentste V2.2)";

      const groupOthers = document.createElement('optgroup');
      groupOthers.label = "📍 Overige Bedieningen (Hiërarchisch Gekoppeld)";

      // Sort items
      const sorted = [...allItems].sort((a,b) => a.name.localeCompare(b.name));

      sorted.forEach(loc => {
        const opt = document.createElement('option');
        opt.value = loc.id;
        const isDetailed = (rawDetailedTerminals && rawDetailedTerminals[loc.id]);
        opt.textContent = `${loc.name} ${loc.has_bi ? '(Reeds BI)' : '(Nog geen BI)'}`;
        if (isDetailed) {
          groupDetailed.appendChild(opt);
        } else {
          groupOthers.appendChild(opt);
        }
      });

      select.appendChild(groupDetailed);
      select.appendChild(groupOthers);

      select.value = currentSelectedBiTerminalId;
    }

    function onBiTerminalSelected(termId) {
      currentSelectedBiTerminalId = termId;
      renderBiDocument(termId);
    }

    // Resolve BI Document (combines pre-resolved data, custom versions, and applied proposals)
    function getResolvedBiForTerminal(termId) {
      let baseBi = rawResolvedBIs[termId];
      if (!baseBi) {
        // Fallback to CRO Brittaniadok
        baseBi = rawResolvedBIs['cro_brit'];
      }
      // Clone baseBi
      let bi = JSON.parse(JSON.stringify(baseBi));

      // Apply custom version from LocalStorage if exists
      if (customVersionsStore[termId]) {
        const custom = customVersionsStore[termId];
        bi.metadata.huidige_versie = custom.huidige_versie;
        bi.metadata.versie_datum = custom.versie_datum;
        bi.metadata.auteurs = custom.auteurs || bi.metadata.auteurs;
        bi.versiebeheer = custom.versiebeheer || bi.versiebeheer;
      }

      // Check if any PPGI proposal was applied to this terminal
      rawPpgiProposals.forEach(prop => {
        if (appliedProposalsStore[prop.id]) {
          // If proposal applies to this terminal or its zone/bundel
          if (prop.id === 'PROP-2026-001' && termId === 'cro_brit') {
            // Procedure formalized
            bi.procedures.procedure_2_rangering_spoor_872 = [
              {"stap": 1, "titel": "Toelating & Poort", "beschrijving": "Voor rangeringen van SA C-RO tot op spoor 872 laat de bediende de poort openen door CRO Security."},
              {"stap": 2, "titel": "Slot aanvragen Blok 7", "beschrijving": "Meld je via de slottelefoon aan bij Blok 7 en vraag slot 321FR om rangeringen uit te voeren tussen de terminal en spoor 872. OPGELET: Tijdens rangeringen zijn ritten naar Ramskapelle verboden!"},
              {"stap": 3, "titel": "OW 17 & Stuitklamp", "beschrijving": "Activeer OW 17 en leg stuitklamp 321 open met sleutel 321."},
              {"stap": 4, "titel": "Rangering uitvoeren", "beschrijving": "Voer de rangering uit. Beëindig de rangering ALTIJD op de spooraansluiting C-RO, nooit op spoor 872."},
              {"stap": 5, "titel": "Vergrendeling herstellen", "beschrijving": "Sluit de stuitklamp, vergrendel sleutel 321 in het Siemensslot (naar rechts draaien) en geef slot 321FR terug aan Blok 7."}
            ];
          }
          if (prop.id === 'PROP-2026-002' && termId === 'cro_brit') {
            if (!bi.veiligheid_en_risicos.some(r => r.omschrijving.includes('Ramskapelle niet toegelaten'))) {
              bi.veiligheid_en_risicos.push({
                "type": "PPGI Veiligheidsclausule",
                "omschrijving": "Tijdens het uitvoeren van rangeringen van/naar C-RO tot op spoor 872 zijn ritten van en naar Bundel Ramskapelle NIET toegelaten. Rangering altijd beëindigen op de spooraansluiting C-RO, nooit op spoor 872.",
                "bron": "PP-321-Brugge v37.0"
              });
            }
          }
          if (prop.id === 'PROP-2026-004') {
            // Add mailbox Blok 7 if not present
            if (!bi.contactpersonen.realtime.some(c => c.dienst.includes('Mailbox Blok 7'))) {
              bi.contactpersonen.realtime.push({
                "dienst": "Mailbox Blok 7 Infrabel",
                "rol": "Schriftelijke overdrachten (Bijlage 1.11)",
                "telefoon": "rdc.nw.blok7@infrabel.be",
                "niveau": "Niveau 3: Seinhuis Blok 7"
              });
            }
          }
        }
      });

      return bi;
    }

    // Render BI Document
    function renderBiDocument(termId) {
      const bi = getResolvedBiForTerminal(termId);
      if (!bi) return;

      const container = document.getElementById('biDocumentCard');
      const breadcrumbs = document.getElementById('biBreadcrumbsContainer');

      // 1. Render Breadcrumbs
      const h = bi.hierarchie_levels;
      breadcrumbs.innerHTML = `
        <div class="bi-crumb-card" onclick="openMasterDataModal('operator')">
          <span class="bi-crumb-level">Niveau 1: Operator</span>
          <span class="bi-crumb-name">🚆 ${h.level_1_operator.naam}</span>
        </div>
        <span class="bi-crumb-arrow">➔</span>
        <div class="bi-crumb-card" onclick="openMasterDataModal('regio')">
          <span class="bi-crumb-level">Niveau 2: Regio</span>
          <span class="bi-crumb-name">🗺️ ${h.level_2_regio.naam}</span>
        </div>
        <span class="bi-crumb-arrow">➔</span>
        <div class="bi-crumb-card" onclick="openMasterDataModal('zone')">
          <span class="bi-crumb-level">Niveau 3: Zone</span>
          <span class="bi-crumb-name">⚓ ${h.level_3_zone.naam}</span>
        </div>
        <span class="bi-crumb-arrow">➔</span>
        <div class="bi-crumb-card" onclick="openMasterDataModal('moederbundel')">
          <span class="bi-crumb-level">Niveau 4: Moederbundel</span>
          <span class="bi-crumb-name">🟡 ${h.level_4_moederbundel.naam}</span>
        </div>
        <span class="bi-crumb-arrow">➔</span>
        <div class="bi-crumb-card" style="border-color:#3b82f6; background:rgba(37,99,235,0.15);">
          <span class="bi-crumb-level" style="color:#60a5fa;">Niveau 5: Terminal</span>
          <span class="bi-crumb-name" style="color:#93c5fd;">⭐ ${h.level_5_terminal.naam}</span>
        </div>
      `;

      // 2. Render Document Header & Body
      let proceduresHtml = '';
      if (bi.procedures) {
        for (const [procKey, steps] of Object.entries(bi.procedures)) {
          let procTitle = "Bedieningsprocedure";
          if (procKey === 'procedure_1_toegang') procTitle = "Procedure 1: Toegang tot de Terminal (Aanvoer)";
          else if (procKey === 'procedure_2_rangering_spoor_872') procTitle = "Procedure 2: Rangeringen van/naar Terminal tot op Spoor 872";
          else if (procKey === 'procedure_3_verlaten') procTitle = "Procedure 3: Verlaten van de Terminal (Afvoer)";

          proceduresHtml += `
            <div style="margin-top: 14px; margin-bottom: 18px;">
              <h4 style="color:#38bdf8; font-size:14px; margin-bottom:8px; font-weight:800;">${procTitle}</h4>
              <div class="bi-step-list">
                ${steps.map(s => `
                  <div class="bi-step-item">
                    <div class="bi-step-num">${s.stap}</div>
                    <div class="bi-step-text">
                      <strong>${s.titel}</strong>
                      <p>${s.beschrijving}</p>
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>
          `;
        }
      }

      // Changelog / Versions Table
      let changelogHtml = `
        <table class="bi-table">
          <thead>
            <tr>
              <th style="width: 80px;">Versie</th>
              <th style="width: 110px;">Datum</th>
              <th>Uitgevoerde Wijzigingen & Autorisatie</th>
            </tr>
          </thead>
          <tbody>
            ${(bi.versiebeheer || []).slice().reverse().map(v => `
              <tr>
                <td><strong style="color:#38bdf8;">v${v.versie}</strong></td>
                <td>${v.datum}</td>
                <td>${v.wijziging}</td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;

      // Realtime Contacts Table
      let realtimeContactsHtml = `
        <table class="bi-table">
          <thead>
            <tr>
              <th>Dienst / Functie</th>
              <th>Rol / Verantwoordelijkheid</th>
              <th>Telefoon / Contact</th>
              <th>Herkomst Brongegevens</th>
            </tr>
          </thead>
          <tbody>
            ${bi.contactpersonen.realtime.map(c => `
              <tr>
                <td><strong>${c.dienst}</strong></td>
                <td>${c.rol}</td>
                <td><code style="color:#38bdf8; font-weight:700;">${c.telefoon}</code></td>
                <td><span class="badge-level badge-level-3">${c.niveau || 'Gelaagd'}</span></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;

      // Emergency Contacts Table
      let emergencyContactsHtml = `
        <table class="bi-table">
          <thead>
            <tr>
              <th>Nooddienst</th>
              <th>Rol</th>
              <th>Telefoon</th>
              <th>Niveau</th>
            </tr>
          </thead>
          <tbody>
            ${bi.contactpersonen.calamiteiten.map(c => `
              <tr>
                <td><strong>${c.dienst}</strong></td>
                <td>${c.rol}</td>
                <td><strong style="color:#ef4444; font-size:14px;">${c.telefoon}</strong></td>
                <td><span class="badge-level badge-level-1">${c.niveau}</span></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;

      // Risks Table
      let risksHtml = `
        <table class="bi-table">
          <thead>
            <tr>
              <th style="width: 180px;">Categorie</th>
              <th>Veiligheidsvoorschrift & Maatregel</th>
              <th style="width: 200px;">Bronniveau</th>
            </tr>
          </thead>
          <tbody>
            ${bi.veiligheid_en_risicos.map(r => `
              <tr>
                <td><span class="badge-level badge-level-2">${r.type}</span></td>
                <td>${r.omschrijving}</td>
                <td><small style="color:#94a3b8;">${r.bron}</small></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      `;

      container.innerHTML = `
        <!-- Header Banner -->
        <div class="bi-doc-header-banner">
          <div class="bi-doc-branding">
            <span class="bi-doc-logo">DB</span>
            <div class="bi-doc-title-box">
              <h1>${bi.metadata.titel.toUpperCase()}</h1>
              <p>Bedieningsinstructie Private Spooraansluiting & Moederbundel • DB Cargo Belgium</p>
            </div>
          </div>
          <div class="bi-doc-version-pill">
            <span>Versie:</span>
            <strong>v${bi.metadata.huidige_versie}</strong>
            <span style="opacity:0.6;">(${bi.metadata.versie_datum})</span>
          </div>
        </div>

        <!-- Meta Grid -->
        <div class="bi-meta-grid">
          <div class="bi-meta-cell">
            <span class="bi-meta-label">Documentcode</span>
            <span class="bi-meta-val">${bi.metadata.documentcode}</span>
          </div>
          <div class="bi-meta-cell">
            <span class="bi-meta-label">Auteurs</span>
            <span class="bi-meta-val">${bi.metadata.auteurs}</span>
          </div>
          <div class="bi-meta-cell">
            <span class="bi-meta-label">Bronreferentie</span>
            <span class="bi-meta-val">${bi.metadata.bron_referentie}</span>
          </div>
          <div class="bi-meta-cell">
            <span class="bi-meta-label">Autorisatie & Goedkeuring</span>
            <span class="bi-meta-val">${bi.metadata.autorisatie_functionaris} (${bi.metadata.goedkeuring_systeem})</span>
          </div>
        </div>

        <!-- Body Chapters -->
        <div class="bi-doc-body">
          
          <!-- H1: Doel & Identificatie -->
          <div class="bi-chapter">
            <div class="bi-chapter-title">1. DOEL EN IDENTIFICATIE DOCUMENT</div>
            <div class="bi-chapter-content">
              <p><strong>Doel:</strong> ${rawHierarchicalLevels.operator.doel}</p>
              <p style="margin-top:6px;"><strong>Gebruikersgroep:</strong> ${bi.metadata.gebruikersgroep}</p>
              <p style="margin-top:6px;"><strong>Ingangsdatum & Goedkeuring:</strong> Deze bedieningsinstructie treedt in werking per ${bi.metadata.autorisatie_ingangsdatum} en is geautoriseerd door ${bi.metadata.autorisatie_functionaris} via ${bi.metadata.goedkeuring_systeem}.</p>
            </div>
          </div>

          <!-- H2: Contactpersonen -->
          <div class="bi-chapter">
            <div class="bi-chapter-title">2. CONTACTPERSONEN (REAL-TIME & OPERATIONEEL)</div>
            <div class="bi-chapter-content">
              <p style="margin-bottom:8px;">Onderstaande tabel groepeert de operationele contacten over de verschillende hiërarchische niveaus (Operator, Seinhuis, Haven en Terminal):</p>
              ${realtimeContactsHtml}
            </div>
          </div>

          <!-- H3: Wat te doen bij calamiteiten -->
          <div class="bi-chapter">
            <div class="bi-chapter-title">3. WAT TE DOEN BIJ CALAMITEITEN</div>
            <div class="bi-chapter-content">
              <div class="bi-callout-danger">
                <strong>🚨 NOODPROCEDURE BIJ ONGEVAL OF INCIDENT</strong><br/>
                1. Breng de beweging onmiddellijk tot stilstand en beveilig tegen ontijdig rollen.<br/>
                2. Breng jezelf en derden in veiligheid. Verleen eerste hulp indien mogelijk.<br/>
                3. Bel direct de bevoegde noodcentrale (112 voor hulpdiensten; Infrabel Rode Telefoon bij spoorincident).<br/>
                4. Verwittig de DB Cargo NOC Shiftleader (+32 3 545 02 33) en de lokale Dispatcher Zeebrugge (+32 50 33 03 25).
              </div>
              <h4 style="color:#ef4444; font-size:13px; font-weight:800; margin: 12px 0 6px 0;">Noodnummers & Dispatching:</h4>
              ${emergencyContactsHtml}
            </div>
          </div>

          <!-- H4: Overzicht van de installaties -->
          <div class="bi-chapter">
            <div class="bi-chapter-title">4. OVERZICHT VAN DE INSTALLATIES</div>
            <div class="bi-chapter-content">
              <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:14px; margin-bottom:12px;">
                <div style="background:#131d31; padding:12px; border-radius:6px; border:1px solid #1e293b;">
                  <strong style="color:#38bdf8;">📍 Situering & Bereikbaarheid:</strong>
                  <p style="margin-top:4px;"><strong>Adres:</strong> ${bi.installaties.situering.adres}</p>
                  <p><strong>Bereikbaarheid trein:</strong> ${bi.installaties.situering.bereikbaarheid.trein}</p>
                  <p><strong>Bereikbaarheid auto:</strong> ${bi.installaties.situering.bereikbaarheid.auto}</p>
                </div>
                <div style="background:#131d31; padding:12px; border-radius:6px; border:1px solid #1e293b;">
                  <strong style="color:#38bdf8;">🟡 Moederbundel (${bi.installaties.moederbundel.naam}):</strong>
                  <p style="margin-top:4px;"><strong>Seininrichting:</strong> ${bi.installaties.moederbundel.seinen_info || 'Geen vaste seinen'}</p>
                  <p><strong>Bovenleiding:</strong> ${bi.installaties.moederbundel.bovenleiding_info || 'Niet geëlektrificeerd'}</p>
                  <p><strong>Tankinstallatie:</strong> ${bi.installaties.moederbundel.tankinstallatie || 'Geen'}</p>
                </div>
              </div>
              <div style="background:#131d31; padding:12px; border-radius:6px; border:1px solid #1e293b;">
                <strong style="color:#38bdf8;">🔒 Private Aansluiting Infrastructuur:</strong>
                <p style="margin-top:4px;"><strong>Toegangsspoor:</strong> ${bi.installaties.terminal.toegangsspoor || 'NVT'}</p>
                <p><strong>Sporen terminal:</strong> ${bi.installaties.terminal.terminal_sporen || 'Bedieningssporen'}</p>
                <p><strong>Beveiligingstoestellen Infrabel:</strong> ${bi.installaties.terminal.beveiliging_infrabel || 'Geen'}</p>
                <p><strong>Richting lading:</strong> ${bi.installaties.terminal.richting_lading || 'Standaard'}</p>
              </div>
            </div>
          </div>

          <!-- H5: Risico's op deze site -->
          <div class="bi-chapter">
            <div class="bi-chapter-title">5. VEILIGHEID EN RISICO'S OP DEZE SITE</div>
            <div class="bi-chapter-content">
              <p style="margin-bottom:8px;">Onderstaande veiligheidsvoorschriften cascaderen van Operatorniveau (Niveau 1), Zoneniveau (Niveau 3) en Terminalniveau (Niveau 5):</p>
              ${risksHtml}
            </div>
          </div>

          <!-- H6: Plaatselijke regelgeving & Snelheden -->
          <div class="bi-chapter">
            <div class="bi-chapter-title">6. PLAATSELIJKE REGELGEVING & SNELHEDEN</div>
            <div class="bi-chapter-content">
              <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:10px; margin-bottom:12px;">
                <div style="background:#131d31; padding:10px 14px; border-radius:6px; border:1px solid #1e293b;">
                  <span style="font-size:11px; color:#94a3b8; font-weight:700;">BUNDELS & VERBINDINGSLIJNEN</span>
                  <div style="font-size:16px; font-weight:900; color:#38bdf8; margin-top:2px;">${bi.plaatselijke_regelgeving.snelheden.bundel}</div>
                </div>
                <div style="background:#131d31; padding:10px 14px; border-radius:6px; border:1px solid #1e293b;">
                  <span style="font-size:11px; color:#94a3b8; font-weight:700;">AANSLUITINGSSPOREN</span>
                  <div style="font-size:16px; font-weight:900; color:#f59e0b; margin-top:2px;">${bi.plaatselijke_regelgeving.snelheden.aansluiting}</div>
                </div>
                <div style="background:#131d31; padding:10px 14px; border-radius:6px; border:1px solid #1e293b;">
                  <span style="font-size:11px; color:#94a3b8; font-weight:700;">KADEN & LOODSEN</span>
                  <div style="font-size:16px; font-weight:900; color:#ef4444; margin-top:2px;">${bi.plaatselijke_regelgeving.snelheden.laadkade}</div>
                </div>
              </div>
              <div class="bi-callout-warning">
                <strong>🌪️ IMMOBILISATIEVOORSCHRIFT:</strong> ${bi.plaatselijke_regelgeving.immobilisatie}
              </div>
            </div>
          </div>

          <!-- H7: Bedieningsinstructie (Stappenplannen) -->
          <div class="bi-chapter">
            <div class="bi-chapter-title">7. BEDIENINGSINSTRUCTIE (STAPPENPLANNEN)</div>
            <div class="bi-chapter-content">
              <p>Volg onderstaande chronologische stappenplannen strikt op bij het uitvoeren van bedieningen:</p>
              ${proceduresHtml}
            </div>
          </div>

          <!-- H8: Versiehistoriek & Wijzigingenlog -->
          <div class="bi-chapter">
            <div class="bi-chapter-title">8. VERSIEBEHEER & WIJZIGINGENLOGBOEK (CHANGELOG)</div>
            <div class="bi-chapter-content">
              <p style="margin-bottom:8px;">Bij elke herziening of generatie van deze bedieningsinstructie worden de specifieke wijzigingen en autorisaties hieronder vastgelegd:</p>
              ${changelogHtml}
            </div>
          </div>

        </div>
      `;
    }

    // Modal: Nieuwe Versie Genereren
    function openNewVersionModal() {
      const bi = getResolvedBiForTerminal(currentSelectedBiTerminalId);
      if (!bi) return;

      const modal = document.getElementById('newVersionModal');
      const intro = document.getElementById('newVersionModalIntro');
      const verInput = document.getElementById('newVersionNumberInput');
      const dateInput = document.getElementById('newVersionDateInput');
      const authorInput = document.getElementById('newVersionAuthorInput');
      const changelogInput = document.getElementById('newVersionChangelogInput');

      intro.innerHTML = `Genereer een nieuwe officiële versie van de Bedieningsinstructie voor <strong>${bi.metadata.terminal_naam}</strong> (huidige versie is v${bi.metadata.huidige_versie}).`;

      // Suggest next minor version (e.g. 2.2 -> 2.3)
      const currentVerNum = parseFloat(bi.metadata.huidige_versie) || 1.0;
      verInput.value = (currentVerNum + 0.1).toFixed(1);

      // Today's date YYYY-MM-DD
      const now = new Date();
      dateInput.value = now.toISOString().split('T')[0];

      changelogInput.value = '';
      modal.classList.add('active');
    }

    function closeNewVersionModal() {
      const modal = document.getElementById('newVersionModal');
      if (modal) modal.classList.remove('active');
    }

    function submitNewBiVersion() {
      const verInput = document.getElementById('newVersionNumberInput');
      const dateInput = document.getElementById('newVersionDateInput');
      const authorInput = document.getElementById('newVersionAuthorInput');
      const changelogInput = document.getElementById('newVersionChangelogInput');

      const newVer = (verInput.value || '').trim();
      const newDate = (dateInput.value || '').trim();
      const newAuthor = (authorInput.value || '').trim();
      const newChanges = (changelogInput.value || '').trim();

      if (!newVer || !newChanges) {
        alert('Vul a.u.b. een versienummer en een omschrijving van de wijzigingen (changelog) in.');
        return;
      }

      // Convert date to DD-MM-YYYY format
      let formattedDate = newDate;
      if (newDate.includes('-')) {
        const parts = newDate.split('-');
        if (parts.length === 3 && parts[0].length === 4) {
          formattedDate = `${parts[2]}-${parts[1]}-${parts[0]}`;
        }
      }

      const termId = currentSelectedBiTerminalId;
      const bi = getResolvedBiForTerminal(termId);

      // Clone existing versions
      let versions = bi.versiebeheer ? JSON.parse(JSON.stringify(bi.versiebeheer)) : [];
      versions.push({
        "versie": newVer,
        "datum": formattedDate,
        "wijziging": newChanges
      });

      // Update custom store
      customVersionsStore[termId] = {
        "huidige_versie": newVer,
        "versie_datum": formattedDate,
        "auteurs": newAuthor,
        "versiebeheer": versions
      };

      try {
        localStorage.setItem(STORAGE_CUSTOM_BI_VERSIONS_KEY, JSON.stringify(customVersionsStore));
      } catch(e) { console.error('Error saving version to localStorage', e); }

      closeNewVersionModal();
      renderBiDocument(termId);
      showToast(`✓ Versie v${newVer} succesvol gegenereerd en geregistreerd in het changelog!`, 'success');
    }

    // Print Document / PDF Trigger
    function printBiDocument() {
      window.print();
    }

    // Modal: Master Data Inspection (Levels 1 to 4)
    function openMasterDataModal(levelKey) {
      const modal = document.getElementById('masterDataModal');
      const title = document.getElementById('masterDataModalTitle');
      const body = document.getElementById('masterDataModalBody');

      let contentHtml = '';

      if (levelKey === 'operator' || !levelKey) {
        const op = rawHierarchicalLevels.operator;
        title.innerHTML = `🏢 Niveau 1: Bedrijf / Operator (${op.naam})`;
        contentHtml = `
          <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid #334155; margin-bottom:14px;">
            <p><strong>Doel:</strong> ${op.doel}</p>
            <p style="margin-top:6px;"><strong>Autorisatie:</strong> ${op.autorisatie_functionaris} (${op.goedkeuring_systeem})</p>
            <p style="margin-top:6px;"><strong>Gebruikersgroep:</strong> ${op.gebruikersgroep}</p>
          </div>
          <h4 style="color:#38bdf8; font-size:13px; font-weight:800; margin: 10px 0;">Algemene Bedrijfsvoorschriften (Cascaderen naar ELKE BI):</h4>
          <ul style="padding-left:20px; line-height:1.6; color:#cbd5e1; font-size:13px;">
            ${op.algemene_veiligheidsregels.map(r => `<li>${r}</li>`).join('')}
          </ul>
          <h4 style="color:#ef4444; font-size:13px; font-weight:800; margin: 14px 0 6px 0;">Landelijke Noodcentrales & Dispatch:</h4>
          <table class="bi-table">
            <thead><tr><th>Dienst</th><th>Rol</th><th>Nummer</th></tr></thead>
            <tbody>
              ${op.noodcontacten.map(n => `<tr><td><strong>${n.dienst}</strong></td><td>${n.rol}</td><td><code>${n.telefoon}</code></td></tr>`).join('')}
            </tbody>
          </table>
        `;
      } else if (levelKey === 'regio') {
        const reg = rawHierarchicalLevels.regio.west_vlaanderen;
        title.innerHTML = `🗺️ Niveau 2: Regio (${reg.naam})`;
        contentHtml = `
          <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid #334155; margin-bottom:14px;">
            <p><strong>Infrabel District:</strong> ${reg.infrabel_district}</p>
            <p style="margin-top:6px;"><strong>Permanentie I-TO:</strong> ${reg.permanentie_ito}</p>
            <p style="margin-top:6px;"><strong>Traffic Officer Area NW:</strong> ${reg.traffic_officer_nw}</p>
            <p style="margin-top:6px;"><strong>SSP Zone:</strong> ${reg.ssp_zone}</p>
          </div>
          <p style="font-size:13px; color:#94a3b8; line-height:1.5;">Regio-gegevens garanderen dat bij incidenten in West-Vlaanderen onmiddellijk contact wordt opgenomen met de bevoegde Traffic Officer en Permanentie I-TO van Area North-West.</p>
        `;
      } else if (levelKey === 'zone') {
        const bi = getResolvedBiForTerminal(currentSelectedBiTerminalId);
        const zId = bi.hierarchie_levels.level_3_zone.code || 'zeebrugge';
        const z = rawHierarchicalLevels.zones[zId] || rawHierarchicalLevels.zones['zeebrugge'];
        title.innerHTML = `⚓ Niveau 3: Zone / Hub (${z.naam})`;
        contentHtml = `
          <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid #334155; margin-bottom:14px;">
            <p><strong>Centraal Seinhuis:</strong> ${z.centraal_seinhuis}</p>
            ${z.havenautoriteit ? `<p style="margin-top:6px;"><strong>Havenkapiteinsdienst:</strong> ${z.havenautoriteit.naam} (${z.havenautoriteit.telefoon}) • VHF: ${z.havenautoriteit.vhf_kanalen}</p>` : ''}
          </div>
          <h4 style="color:#38bdf8; font-size:13px; font-weight:800; margin:10px 0;">Seinhuis Contactpersonen:</h4>
          <table class="bi-table">
            <thead><tr><th>Functie</th><th>Rol</th><th>Contact</th></tr></thead>
            <tbody>
              ${z.seinhuis_contacten.map(c => `<tr><td><strong>${c.dienst}</strong></td><td>${c.rol}</td><td><code>${c.telefoon}</code></td></tr>`).join('')}
            </tbody>
          </table>
          <h4 style="color:#f59e0b; font-size:13px; font-weight:800; margin:14px 0 6px 0;">Specifieke Zonerisico's:</h4>
          <ul style="padding-left:20px; line-height:1.6; color:#cbd5e1; font-size:13px;">
            ${z.zone_risicos.map(r => `<li>${r}</li>`).join('')}
          </ul>
        `;
      } else if (levelKey === 'moederbundel') {
        const bi = getResolvedBiForTerminal(currentSelectedBiTerminalId);
        const mbId = bi.hierarchie_levels.level_4_moederbundel.code || 'ramskapelle';
        const mb = rawHierarchicalLevels.moederbundels[mbId] || rawHierarchicalLevels.moederbundels['ramskapelle'];
        title.innerHTML = `🟡 Niveau 4: Moederbundel (${mb.naam})`;
        contentHtml = `
          <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid #334155; margin-bottom:14px;">
            <p><strong>Infrabel PPGI Referentie:</strong> ${mb.ppgi_referentie}</p>
            <p style="margin-top:6px;"><strong>SSP Referentie:</strong> ${mb.ssp_referentie}</p>
            <p style="margin-top:6px;"><strong>Beseind:</strong> ${mb.beseind ? 'Ja (met stopseinen en dwergseinen)' : 'Nee'}</p>
            <p style="margin-top:6px;"><strong>Bovenleiding:</strong> ${mb.bovenleiding_info}</p>
            <p style="margin-top:6px;"><strong>Tankinstallatie:</strong> ${mb.tankinstallatie}</p>
            <p style="margin-top:6px;"><strong>Cameratoezicht:</strong> ${mb.cameras}</p>
          </div>
          ${mb.bundel_sporen && mb.bundel_sporen.length > 0 ? `
            <h4 style="color:#38bdf8; font-size:13px; font-weight:800; margin:10px 0;">Bundelsporen & Beveiliging:</h4>
            <table class="bi-table">
              <thead><tr><th>Spoor</th><th>Type</th><th>Beveiliging</th></tr></thead>
              <tbody>
                ${mb.bundel_sporen.map(s => `<tr><td><strong>${s.spoor}</strong></td><td>${s.type}</td><td><code>${s.beveiliging}</code></td></tr>`).join('')}
              </tbody>
            </table>
          ` : ''}
        `;
      }

      body.innerHTML = contentHtml;
      modal.classList.add('active');
    }

    function closeMasterDataModal() {
      const modal = document.getElementById('masterDataModal');
      if (modal) modal.classList.remove('active');
    }

    // ========================================================
    // PPGI AUDIT REVIEW PROPOSALS RENDERER
    // ========================================================
    function renderPpgiProposals() {
      const container = document.getElementById('ppgiProposalsContainer');
      if (!container) return;

      let appliedCount = 0;
      let highCount = 0;
      let medCount = 0;

      rawPpgiProposals.forEach(p => {
        if (appliedProposalsStore[p.id]) appliedCount++;
        if (p.urgentie === 'HOOG') highCount++;
        if (p.urgentie === 'MEDIUM') medCount++;
      });

      // Update badge in top header
      const ppgiBadge = document.getElementById('ppgiBadgeCount');
      if (ppgiBadge) {
        const remaining = rawPpgiProposals.length - appliedCount;
        ppgiBadge.textContent = remaining;
        ppgiBadge.style.display = remaining > 0 ? 'inline-block' : 'none';
      }

      // Update metrics
      const mApplied = document.getElementById('ppgiMetricApplied');
      const mHigh = document.getElementById('ppgiMetricHigh');
      const mMed = document.getElementById('ppgiMetricMedium');
      if (mApplied) mApplied.textContent = appliedCount;
      if (mHigh) mHigh.textContent = highCount;
      if (mMed) mMed.textContent = medCount;

      container.innerHTML = rawPpgiProposals.map(prop => {
        const isApplied = !!appliedProposalsStore[prop.id];
        return `
          <div class="ppgi-proposal-card urgency-${prop.urgentie_badge}">
            <div class="ppgi-card-header">
              <div class="ppgi-card-title-group">
                <span class="ppgi-prop-id">${prop.id}</span>
                <span class="ppgi-prop-title">${prop.titel}</span>
              </div>
              <span class="badge-urgency badge-urgency-${prop.urgentie_badge}">${prop.urgentie} URGENTIE</span>
            </div>

            <div class="ppgi-card-body">
              <div class="ppgi-ref-badge-row">
                <span>📄 Bron: <strong class="ppgi-ref-tag">${prop.bron_document}</strong></span>
                <span>📌 Sectie: <strong class="ppgi-ref-tag">${prop.bron_sectie}</strong></span>
                <span>🏛️ Toepassingsniveau: <strong class="ppgi-ref-tag" style="color:#38bdf8;">${prop.niveau}</strong></span>
              </div>

              <!-- Side by side Diff comparison -->
              <div class="ppgi-diff-grid">
                <div class="ppgi-diff-box ppgi-diff-current">
                  <div class="ppgi-diff-label">❌ Huidige situatie in BI (v2.2):</div>
                  <p>${prop.huidige_waarde_bi}</p>
                </div>
                <div class="ppgi-diff-box ppgi-diff-proposed">
                  <div class="ppgi-diff-label">✅ Voorgestelde aanpassing conform Infrabel PPGI:</div>
                  <p>${prop.voorgestelde_waarde_ppgi}</p>
                </div>
              </div>

              <div class="ppgi-rationale-box">
                <strong>💡 Motivering & Veiligheidsanalyse:</strong> ${prop.motivering}
              </div>
            </div>

            <div class="ppgi-card-footer">
              <span style="font-size:12px; color:#94a3b8;">
                Status: <strong>${isApplied ? '✓ Reeds doorgevoerd in v2.3' : prop.status}</strong>
              </span>

              ${isApplied ? `
                <div class="btn-ppgi-applied">
                  <span>✓</span> Toegepast in BI (Zie Changelog)
                </div>
              ` : `
                <button class="btn-ppgi-apply" onclick="applyPpgiProposal('${prop.id}')">
                  <span>✓</span> Pas Voorstel Toe in BI
                </button>
              `}
            </div>
          </div>
        `;
      }).join('');
    }

    function applyPpgiProposal(propId) {
      const prop = rawPpgiProposals.find(p => p.id === propId);
      if (!prop) return;

      appliedProposalsStore[propId] = true;
      try {
        localStorage.setItem(STORAGE_APPLIED_PROPOSALS_KEY, JSON.stringify(appliedProposalsStore));
      } catch(e) { console.error('Error saving applied proposal to localStorage', e); }

      // Also register a revision changelog entry in CRO Brittaniadok
      const termId = 'cro_brit';
      const bi = getResolvedBiForTerminal(termId);
      let versions = bi.versiebeheer ? JSON.parse(JSON.stringify(bi.versiebeheer)) : [];
      
      const newVer = "2.3";
      const now = new Date();
      const formattedDate = `${String(now.getDate()).padStart(2, '0')}-${String(now.getMonth() + 1).padStart(2, '0')}-${now.getFullYear()}`;

      // Check if we already have an entry for this proposal
      const changeMsg = `Inpassing PPGI wijziging (${prop.id}): ${prop.titel}. Bron: ${prop.bron_document}.`;
      if (!versions.some(v => v.wijziging.includes(prop.id))) {
        versions.push({
          "versie": newVer,
          "datum": formattedDate,
          "wijziging": changeMsg
        });

        customVersionsStore[termId] = {
          "huidige_versie": newVer,
          "versie_datum": formattedDate,
          "auteurs": "Bart VERCAEMPST Teamleader DBC.BE",
          "versiebeheer": versions
        };
        try {
          localStorage.setItem(STORAGE_CUSTOM_BI_VERSIONS_KEY, JSON.stringify(customVersionsStore));
        } catch(e) {}
      }

      renderPpgiProposals();
      showToast(`✓ Voorstel ${prop.id} succesvol toegepast! Schakel naar BI Generator om de wijziging te zien.`, 'success');
    }
    '''
