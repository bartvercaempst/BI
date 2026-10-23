"""
HTML, CSS and JS view components for:
- 📄 BI Generator & PDF Export (IDENTICAL Word/PDF document layout, complete scrolling, full PDF generation)
- 🔍 PPGI Vergelijker & Audit Voorstellen (with diff comparisons and interactive 'Pas toe' actions)
- Master data inspection modal for cascading levels 1-4
"""

import json
import os
import base64

# Load base64 assets if available
ws_dir = os.path.dirname(os.path.abspath(__file__))
b64_path = os.path.join(ws_dir, 'extracted_b64.json')
DB_LOGO_B64 = ""
VERZAMELPUNT_B64 = ""
if os.path.exists(b64_path):
    try:
        with open(b64_path, 'r', encoding='utf-8') as f:
            b64_data = json.load(f)
            DB_LOGO_B64 = b64_data.get('db_logo', '')
            VERZAMELPUNT_B64 = b64_data.get('verzamelpunt', '')
    except Exception as e:
        pass

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
      background: #162032;
      color: #ffffff;
      border: 1.5px solid #475569;
      padding: 0 14px;
      height: 36px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .nav-tab-btn:hover {
      background: #25334d;
      color: #ffffff;
      border-color: #94a3b8;
    }
    .nav-tab-btn.active {
      background: #2563eb;
      color: #ffffff;
      border-color: #93c5fd;
      box-shadow: 0 0 14px rgba(37, 99, 235, 0.6);
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
      background: #162032;
      color: #ffffff;
      border: 1.5px solid #475569;
      padding: 12px 14px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 800;
      text-align: left;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.15s ease;
    }
    .drawer-tab-btn:hover {
      background: #25334d;
      color: #ffffff;
      border-color: #94a3b8;
    }
    .drawer-tab-btn.active {
      background: #2563eb;
      color: #ffffff;
      border-color: #93c5fd;
      box-shadow: 0 0 10px rgba(37, 99, 235, 0.45);
    }

    /* ======================================================== */
    /* VIEW CONTAINERS & SCROLL ARCHITECTURE                    */
    /* ======================================================== */
    .main-container {
      flex: 1 1 auto !important;
      display: flex !important;
      flex-direction: column !important;
      position: relative !important;
      overflow: hidden !important;
      min-height: 0 !important;
      height: calc(100vh - 60px) !important;
      width: 100% !important;
    }

    #mapView {
      width: 100%;
      height: 100%;
      display: flex;
      flex-direction: row;
      position: relative;
      overflow: hidden;
      flex: 1 1 auto;
      min-height: 0;
    }

    #biGeneratorView {
      width: 100%;
      height: 100%;
      flex: 1 1 auto;
      min-height: 0;
      max-height: 100%;
      display: none;
      flex-direction: column;
      overflow-y: scroll !important;
      -webkit-overflow-scrolling: touch;
      background: #0b1120;
      color: #0f172a;
      padding: 20px 24px 80px 24px;
      box-sizing: border-box;
    }

    #ppgiReviewView {
      width: 100%;
      height: 100%;
      flex: 1 1 auto;
      min-height: 0;
      max-height: 100%;
      display: none;
      flex-direction: column;
      overflow-y: scroll !important;
      -webkit-overflow-scrolling: touch;
      background: #0b1120;
      color: #f1f5f9;
      padding: 20px 24px 80px 24px;
      box-sizing: border-box;
    }

    /* ======================================================== */
    /* BI GENERATOR TOOLBAR & BREADCRUMBS                       */
    /* ======================================================== */
    .bi-top-toolbar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      background: #0d1424;
      border: 2px solid #334155;
      padding: 12px 18px;
      border-radius: 10px;
      margin-bottom: 16px;
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.45);
      flex-shrink: 0;
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
      font-weight: 900;
      color: #ffffff;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .bi-select-dropdown {
      background: #131c2e;
      border: 2px solid #475569;
      color: #ffffff;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 800;
      outline: none;
      cursor: pointer;
      min-width: 280px;
      max-width: 100%;
      transition: border-color 0.2s, box-shadow 0.2s;
    }
    .bi-select-dropdown:focus {
      border-color: #38bdf8;
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.35);
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
      border: 1.5px solid #60a5fa;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4);
      transition: all 0.2s;
    }
    .btn-bi-primary:hover {
      background: #1d4ed8;
      border-color: #93c5fd;
      transform: translateY(-1px);
    }
    .btn-bi-success {
      background: #059669;
      color: #ffffff;
      border: 1.5px solid #34d399;
      padding: 8px 14px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 2px 8px rgba(5, 150, 105, 0.4);
      transition: all 0.2s;
    }
    .btn-bi-success:hover {
      background: #047857;
      border-color: #6ee7b7;
      transform: translateY(-1px);
    }
    .btn-bi-secondary {
      background: #1e293b;
      color: #ffffff;
      border: 1.5px solid #475569;
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 800;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s;
    }
    .btn-bi-secondary:hover {
      background: #334155;
      color: #ffffff;
      border-color: #94a3b8;
    }

    /* 5-Level Cascading Hierarchy Breadcrumbs */
    .bi-breadcrumbs-wrap {
      background: #0d1424;
      border: 2px solid #334155;
      padding: 10px 16px;
      border-radius: 10px;
      margin-bottom: 20px;
      flex-shrink: 0;
    }
    .bi-breadcrumbs-title {
      font-size: 11px;
      font-weight: 800;
      color: #ffffff;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      margin-bottom: 8px;
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
      background: #131d31;
      border: 1.5px solid #475569;
      padding: 6px 10px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }
    .bi-crumb-card:hover {
      border-color: #38bdf8;
      background: #1e2c45;
      transform: translateY(-1px);
    }
    .bi-crumb-level {
      font-size: 9px;
      font-weight: 800;
      color: #38bdf8;
      text-transform: uppercase;
    }
    .bi-crumb-name {
      font-size: 12px;
      font-weight: 800;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .bi-crumb-arrow {
      color: #94a3b8;
      font-weight: 900;
      font-size: 14px;
    }

    /* ======================================================== */
    /* IDENTICAL WORD / PDF DOCUMENT STYLING (HIGH CONTRAST)    */
    /* ======================================================== */
    .bi-doc-card {
      background: #ffffff;
      color: #000000;
      font-family: Arial, Helvetica, sans-serif !important;
      width: 100%;
      max-width: 860px;
      margin: 0 auto 50px auto;
      padding: 60px 70px;
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.55);
      border: 1.5px solid #cbd5e1;
      border-radius: 4px;
      box-sizing: border-box;
      line-height: 1.45;
      font-size: 10pt;
    }

    /* Cover Page */
    .bi-cover-page {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      min-height: 700px;
      padding-bottom: 40px;
    }
    .bi-cover-top {
      display: flex;
      justify-content: flex-end;
      align-items: center;
    }
    .bi-cover-center {
      text-align: center;
      margin: 100px 0 80px 0;
    }
    .bi-cover-center h1 {
      font-family: Arial, sans-serif !important;
      font-size: 34pt !important;
      font-weight: bold !important;
      color: #000000 !important;
      margin: 0 0 16px 0 !important;
      letter-spacing: -0.5px;
    }
    .bi-cover-center h2 {
      font-family: Arial, sans-serif !important;
      font-size: 26pt !important;
      font-weight: bold !important;
      color: #000000 !important;
      margin: 0 0 16px 0 !important;
    }
    .bi-cover-center h3 {
      font-family: Arial, sans-serif !important;
      font-size: 16pt !important;
      font-weight: bold !important;
      color: #000000 !important;
      margin: 0 !important;
    }
    .bi-cover-bottom {
      border-top: 1.5px solid #1e293b;
      padding-top: 14px;
      display: flex;
      justify-content: space-between;
      font-size: 9pt;
      font-weight: 600;
      color: #1e293b;
    }

    /* Page Breaks */
    .bi-page-break {
      page-break-after: always;
      break-after: page;
      height: 1px;
      margin: 40px 0;
      border-bottom: 1px dashed #94a3b8;
    }

    /* Running Header in Document */
    .bi-running-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid #164e87;
      padding-bottom: 6px;
      margin-bottom: 24px;
      font-size: 8.5pt;
      font-weight: 600;
      color: #1e293b;
      font-family: Arial, sans-serif;
    }
    .bi-running-header-left {
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: bold;
      color: #000000;
    }

    /* Word Headings (High-Contrast Corporate Blue & Navy) */
    .bi-h1 {
      font-family: Arial, sans-serif !important;
      color: #164e87 !important;
      font-size: 15pt !important;
      font-weight: bold !important;
      margin-top: 28px !important;
      margin-bottom: 12px !important;
      border-bottom: 2.5px solid #164e87 !important;
      padding-bottom: 5px !important;
    }
    .bi-h2 {
      font-family: Arial, sans-serif !important;
      color: #164e87 !important;
      font-size: 12.5pt !important;
      font-weight: bold !important;
      margin-top: 20px !important;
      margin-bottom: 8px !important;
    }
    .bi-h3 {
      font-family: Arial, sans-serif !important;
      color: #0f2942 !important;
      font-size: 10.5pt !important;
      font-weight: bold !important;
      margin-top: 15px !important;
      margin-bottom: 6px !important;
    }

    .bi-p {
      font-family: Arial, sans-serif;
      font-size: 10pt;
      color: #000000;
      margin: 0 0 8px 0;
      line-height: 1.5;
    }
    .bi-p-small {
      font-size: 9pt;
      font-weight: 500;
      color: #1e293b;
      margin: 0 0 6px 0;
    }

    /* Word Tables (Crisp, High-Contrast Borders & Headers) */
    .bi-word-table {
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0 18px 0;
      font-family: Arial, sans-serif;
      font-size: 9.5pt;
      color: #000000;
    }
    .bi-word-table th {
      background-color: #cbd5e1 !important;
      color: #0f172a !important;
      font-weight: 800 !important;
      border: 1.5px solid #334155 !important;
      border-bottom: 2.5px solid #0f172a !important;
      padding: 7px 10px !important;
      text-align: left;
    }
    .bi-word-table td {
      border: 1px solid #475569 !important;
      padding: 7px 10px !important;
      vertical-align: top;
      color: #000000;
    }
    .bi-word-table .bg-grey {
      background-color: #cbd5e1 !important;
      font-weight: 800 !important;
      color: #0f172a !important;
      border: 1.5px solid #334155 !important;
    }
    .bi-word-table .header-group {
      background-color: #e2e8f0 !important;
      font-weight: 800 !important;
      color: #0f172a !important;
      padding: 7px 10px;
      border: 1.5px solid #334155 !important;
    }

    /* Left Color Bar in Contact Tables (High Saturation & Contrast) */
    .bi-bar-red {
      background-color: #b91c1c !important;
      width: 10px !important;
      min-width: 10px !important;
      max-width: 10px !important;
      padding: 0 !important;
    }
    .bi-bar-blue {
      background-color: #0284c7 !important;
      width: 10px !important;
      min-width: 10px !important;
      max-width: 10px !important;
      padding: 0 !important;
    }
    .bi-bar-emergency {
      background-color: #dc2626 !important;
      width: 10px !important;
      min-width: 10px !important;
      max-width: 10px !important;
      padding: 0 !important;
    }
    .bi-bar-grey {
      background-color: #475569 !important;
      width: 10px !important;
      min-width: 10px !important;
      max-width: 10px !important;
      padding: 0 !important;
    }

    /* Stappen Tabel (Bedieningsstappen 7.4.2 & 7.4.4) */
    .bi-step-table {
      width: 100%;
      border-collapse: collapse;
      margin: 12px 0 18px 0;
      font-family: Arial, sans-serif;
      font-size: 9.5pt;
      color: #000000;
    }
    .bi-step-table th {
      background-color: #cbd5e1 !important;
      color: #0f172a !important;
      font-weight: 800 !important;
      border: 1.5px solid #334155 !important;
      border-bottom: 2.5px solid #0f172a !important;
      padding: 7px 10px;
      text-align: left;
    }
    .bi-step-table td {
      border: 1px solid #475569 !important;
      padding: 8px 10px;
      color: #000000;
      vertical-align: top;
    }
    .bi-step-num-cell {
      width: 70px;
      min-width: 70px;
      background-color: #e2e8f0 !important;
      font-weight: 900 !important;
      color: #0f172a !important;
      text-align: center;
      vertical-align: top;
      border-right: 2.5px solid #334155 !important;
    }

    /* Inhoudstafel List (Sharp Dots & Crisp Contrast) */
    .bi-toc-list {
      display: flex;
      flex-direction: column;
      gap: 6px;
      margin: 14px 0 24px 0;
      font-size: 9.5pt;
    }
    .bi-toc-item {
      display: flex;
      justify-content: space-between;
      color: #0f172a;
      text-decoration: none;
      transition: color 0.15s;
    }
    .bi-toc-item:hover {
      color: #164e87;
      text-decoration: underline;
    }
    .bi-toc-item.level-1 {
      font-weight: 800;
      color: #0f172a;
      border-bottom: 1.5px dotted #94a3b8;
      padding: 4px 0;
      margin-top: 4px;
    }
    .bi-toc-item.level-2 {
      padding-left: 20px;
      font-weight: 600;
      color: #1e293b;
    }
    .bi-toc-item.level-3 {
      padding-left: 38px;
      color: #334155;
      font-weight: 500;
    }

    /* Callout Note box (High Contrast Security/Attention Bar) */
    .bi-word-callout {
      border: 1px solid #94a3b8;
      border-left: 5px solid #164e87;
      background-color: #f8fafc;
      padding: 12px 16px;
      margin: 14px 0;
      font-size: 9.5pt;
      line-height: 1.55;
      color: #0f172a;
      border-radius: 0 4px 4px 0;
    }

    /* ======================================================== */
    /* PPGI REVIEWER VIEW STYLES                                */
    /* ======================================================== */
    .ppgi-audit-banner {
      background: #0d1424;
      border: 2px solid #334155;
      border-radius: 12px;
      padding: 20px 24px;
      margin-bottom: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      flex-shrink: 0;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35);
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
      font-weight: 900;
      color: #ffffff;
      margin-bottom: 4px;
    }
    .ppgi-banner-title p {
      font-size: 13px;
      color: #cbd5e1;
      font-weight: 600;
    }
    .ppgi-metrics-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
      gap: 12px;
    }
    .ppgi-metric-card {
      background: #131d31;
      border: 1.5px solid #334155;
      padding: 12px 16px;
      border-radius: 8px;
      text-align: center;
    }
    .ppgi-metric-val {
      font-size: 24px;
      font-weight: 900;
      color: #ffffff;
    }
    .ppgi-metric-label {
      font-size: 11px;
      font-weight: 800;
      color: #94a3b8;
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
    .ppgi-proposal-card.urgency-danger { border-left: 5px solid #ef4444; }
    .ppgi-proposal-card.urgency-warning { border-left: 5px solid #f59e0b; }
    .ppgi-proposal-card.urgency-info { border-left: 5px solid #38bdf8; }

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

    .ppgi-diff-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    @media (max-width: 768px) {
      .ppgi-diff-grid { grid-template-columns: 1fr; }
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
    .btn-ppgi-apply:hover { background: #1d4ed8; }
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
    /* PRINT / PDF GENERATION STYLES (FULL MULTI-PAGE FIX)      */
    /* ======================================================== */
    @media print {
      @page {
        size: A4 portrait;
        margin: 15mm 15mm 15mm 15mm;
      }
      *, *::before, *::after {
        box-shadow: none !important;
        text-shadow: none !important;
      }
      html, body {
        height: auto !important;
        min-height: 100% !important;
        max-height: none !important;
        overflow: visible !important;
        position: static !important;
        background: #ffffff !important;
        color: #000000 !important;
        display: block !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        font-family: Arial, Helvetica, sans-serif !important;
      }
      header, .header-main-tabs, .mobile-hub-bar, .mobile-menu-drawer,
      .mobile-drawer-backdrop, .mobile-nav-pill, .modal-backdrop,
      #mapView, #ppgiReviewView, .bi-top-toolbar, .bi-breadcrumbs-wrap,
      .action-banner, .toast-notification, .sidebar-toggle, .map-legend,
      .detail-overlay, .btn-coord-tool, .bi-app-only {
        display: none !important;
      }
      .main-container {
        display: block !important;
        position: static !important;
        height: auto !important;
        min-height: 0 !important;
        max-height: none !important;
        overflow: visible !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
      }
      #biGeneratorView {
        display: block !important;
        position: static !important;
        height: auto !important;
        min-height: 0 !important;
        max-height: none !important;
        overflow: visible !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        background: #ffffff !important;
      }
      .bi-doc-card {
        display: block !important;
        position: static !important;
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        overflow: visible !important;
        border: none !important;
        box-shadow: none !important;
        margin: 0 !important;
        padding: 0 !important;
        background: #ffffff !important;
      }
      .bi-page-break {
        page-break-after: always !important;
        break-after: page !important;
        height: 0 !important;
        margin: 0 !important;
        border: none !important;
      }
      .bi-word-table, .bi-step-table, tr, td, th {
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }
      .bi-h1, .bi-h2, .bi-h3 {
        page-break-after: avoid !important;
        break-after: avoid !important;
      }
    }
'''

def get_bi_html_markup(locations):
    return f'''
    <!-- VIEW 2: BI GENERATOR & PDF EXPORT -->
    <div id="biGeneratorView">
      
      <!-- Top Action Toolbar -->
      <div class="bi-top-toolbar bi-app-only">
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
      <div class="bi-breadcrumbs-wrap bi-app-only">
        <div class="bi-breadcrumbs-title">
          <span>🏛️ Gelaagde Hiërarchie (Brongegevens Cascadering)</span>
          <span style="font-size: 11px; color: #38bdf8; font-weight: 600;">Klik op een niveau om gedeelde gegevens te inspecteren</span>
        </div>
        <div class="bi-breadcrumbs-list" id="biBreadcrumbsContainer">
          <!-- Rendered via JS -->
        </div>
      </div>

      <!-- Rendered BI Document Preview (IDENTIEK AAN WORD / PDF) -->
      <div class="bi-doc-card" id="biDocumentCard">
        <!-- Rendered via renderBiDocument(terminalId) -->
      </div>
    </div>

    <!-- VIEW 3: PPGI VERGELIJKER & AUDIT VOORSTELLEN -->
    <div id="ppgiReviewView">
      
      <!-- Audit Header Banner -->
      <div class="ppgi-audit-banner bi-app-only">
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
    # Assets for logo and icons
    logo_data_uri = f"data:image/png;base64,{DB_LOGO_B64}" if DB_LOGO_B64 else ""
    verzamelpunt_data_uri = f"data:image/gif;base64,{VERZAMELPUNT_B64}" if VERZAMELPUNT_B64 else ""

    return f'''
    // ========================================================
    // BI GENERATOR & PPGI REVIEW JAVASCRIPT ENGINE
    // ========================================================

    const STORAGE_CUSTOM_BI_VERSIONS_KEY = 'db_cargo_bi_versions_v1';
    const STORAGE_APPLIED_PROPOSALS_KEY = 'db_cargo_applied_proposals_v1';
    const ASSET_DB_LOGO = "{logo_data_uri}";
    const ASSET_VERZAMELPUNT = "{verzamelpunt_data_uri}";

    let currentMainTab = 'map'; // 'map', 'bi', 'ppgi'
    let currentSelectedBiTerminalId = 'cro_brit';
    let customVersionsStore = {{}};
    let appliedProposalsStore = {{}};

    // Initialize custom stores from localStorage
    try {{
      const vRaw = localStorage.getItem(STORAGE_CUSTOM_BI_VERSIONS_KEY);
      if (vRaw) customVersionsStore = JSON.parse(vRaw);
    }} catch(e) {{}}

    try {{
      const pRaw = localStorage.getItem(STORAGE_APPLIED_PROPOSALS_KEY);
      if (pRaw) appliedProposalsStore = JSON.parse(pRaw);
    }} catch(e) {{}}

    // Tab Switcher
    function switchMainTab(tab) {{
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

      // Update Bottom Mobile Pill
      const btnMobMap = document.getElementById('btnMobMap');
      const btnMobBi = document.getElementById('btnMobBi');
      const btnMobPpgi = document.getElementById('btnMobPpgi');
      if (btnMobMap) btnMobMap.classList.toggle('active', tab === 'map');
      if (btnMobBi) btnMobBi.classList.toggle('active', tab === 'bi');
      if (btnMobPpgi) btnMobPpgi.classList.toggle('active', tab === 'ppgi');

      // Toggle Views
      const mapView = document.getElementById('mapView');
      const biView = document.getElementById('biGeneratorView');
      const ppgiView = document.getElementById('ppgiReviewView');

      if (mapView) mapView.style.display = (tab === 'map') ? 'flex' : 'none';
      if (biView) biView.style.display = (tab === 'bi') ? 'flex' : 'none';
      if (ppgiView) ppgiView.style.display = (tab === 'ppgi') ? 'flex' : 'none';

      // Header controls visibility: Hub buttons and Map actions only on map
      const headerCenter = document.querySelector('.header-center');
      if (headerCenter && window.innerWidth > 900) {{
        headerCenter.style.display = (tab === 'map') ? 'flex' : 'none';
      }}

      if (tab === 'map') {{
        setTimeout(() => {{ if (typeof map !== 'undefined' && map.invalidateSize) map.invalidateSize(); }}, 150);
      }} else if (tab === 'bi') {{
        populateBiSelectDropdown();
        renderBiDocument(currentSelectedBiTerminalId);
      }} else if (tab === 'ppgi') {{
        renderPpgiProposals();
      }}
    }}

    // Populate Terminal Dropdown
    function populateBiSelectDropdown() {{
      const select = document.getElementById('biTerminalSelect');
      if (!select || select.children.length > 0) return;

      const groupDetailed = document.createElement('optgroup');
      groupDetailed.label = "⭐ Gedetailleerde Bedieningsinstructies (Recentste V2.2)";

      const groupOthers = document.createElement('optgroup');
      groupOthers.label = "📍 Overige Bedieningen (Hiërarchisch Gekoppeld)";

      // Sort items
      const sorted = [...allItems].sort((a,b) => a.name.localeCompare(b.name));

      sorted.forEach(loc => {{
        const opt = document.createElement('option');
        opt.value = loc.id;
        const isDetailed = (rawDetailedTerminals && rawDetailedTerminals[loc.id]);
        opt.textContent = `${{loc.name}} ${{loc.has_bi ? '(Reeds BI)' : '(Nog geen BI)'}}`;
        if (isDetailed) {{
          groupDetailed.appendChild(opt);
        }} else {{
          groupOthers.appendChild(opt);
        }}
      }});

      select.appendChild(groupDetailed);
      select.appendChild(groupOthers);

      select.value = currentSelectedBiTerminalId;
    }}

    function onBiTerminalSelected(termId) {{
      currentSelectedBiTerminalId = termId;
      renderBiDocument(termId);
    }}

    // Resolve BI Document (combines pre-resolved data, custom versions, and applied proposals)
    function getResolvedBiForTerminal(termId) {{
      let baseBi = rawResolvedBIs[termId];
      if (!baseBi) {{
        baseBi = rawResolvedBIs['cro_brit'];
      }}
      let bi = JSON.parse(JSON.stringify(baseBi));

      // Apply custom version from LocalStorage if exists
      if (customVersionsStore[termId]) {{
        const custom = customVersionsStore[termId];
        bi.metadata.huidige_versie = custom.huidige_versie;
        bi.metadata.versie_datum = custom.versie_datum;
        bi.metadata.auteurs = custom.auteurs || bi.metadata.auteurs;
        bi.versiebeheer = custom.versiebeheer || bi.versiebeheer;
      }}

      // Apply any proposals
      rawPpgiProposals.forEach(prop => {{
        if (appliedProposalsStore[prop.id]) {{
          if (prop.id === 'PROP-2026-001' && termId === 'cro_brit') {{
            bi.procedures.procedure_2_rangering_spoor_872 = [
              {{"stap": 1, "titel": "Toelating & Poort", "beschrijving": "Voor rangeringen van SA C-RO tot op spoor 872 laat de bediende de poort openen door CRO Security."}},
              {{"stap": 2, "titel": "Slot aanvragen Blok 7", "beschrijving": "Meld je via de slottelefoon aan bij Blok 7 en vraag slot 321FR om rangeringen uit te voeren tussen de terminal en spoor 872. OPGELET: Tijdens rangeringen zijn ritten naar Ramskapelle verboden!"}},
              {{"stap": 3, "titel": "OW 17 & Stuitklamp", "beschrijving": "Activeer OW 17 en leg stuitklamp 321 open met sleutel 321."}},
              {{"stap": 4, "titel": "Rangering uitvoeren", "beschrijving": "Voer de rangering uit. Beëindig de rangering ALTIJD op de spooraansluiting C-RO, nooit op spoor 872."}},
              {{"stap": 5, "titel": "Vergrendeling herstellen", "beschrijving": "Sluit de stuitklamp, vergrendel sleutel 321 in het Siemensslot (naar rechts draaien) en geef slot 321FR terug aan Blok 7."}}
            ];
          }}
          if (prop.id === 'PROP-2026-002' && termId === 'cro_brit') {{
            if (!bi.veiligheid_en_risicos.some(r => r.omschrijving.includes('Ramskapelle niet toegelaten'))) {{
              bi.veiligheid_en_risicos.push({{
                "type": "PPGI Veiligheidsclausule",
                "omschrijving": "Tijdens het uitvoeren van rangeringen van/naar C-RO tot op spoor 872 zijn ritten van en naar Bundel Ramskapelle NIET toegelaten. Rangering altijd beëindigen op de spooraansluiting C-RO, nooit op spoor 872.",
                "bron": "PP-321-Brugge v37.0"
              }});
            }}
          }}
          if (prop.id === 'PROP-2026-004' && bi.hierarchie_levels.level_3_zone.code === 'zeebrugge') {{
            if (!bi.contactpersonen.realtime.some(c => c.dienst.includes('Mailbox Blok 7'))) {{
              bi.contactpersonen.realtime.push({{
                "dienst": "Mailbox Blok 7 Infrabel",
                "rol": "Schriftelijke overdrachten (Bijlage 1.11)",
                "telefoon": "rdc.nw.blok7@infrabel.be",
                "niveau": "Niveau 3: Seinhuis Blok 7"
              }});
            }}
          }}
        }}
      }});

      return bi;
    }}

    // Render BI Document (IDENTIEK AAN WORD / PDF MET VOLLEDIGE INHOUD)
    function renderBiDocument(termId) {{
      const terminalId = termId;
      const bi = getResolvedBiForTerminal(termId);
      if (!bi) return;
      const infra = bi.infrastructuur || (bi.installaties && bi.installaties.terminal) || {{}};

      const container = document.getElementById('biDocumentCard');
      const breadcrumbs = document.getElementById('biBreadcrumbsContainer');

      // 1. Render Breadcrumbs
      const h = bi.hierarchie_levels;
      breadcrumbs.innerHTML = `
        <div class="bi-crumb-card" onclick="openMasterDataModal('operator')">
          <span class="bi-crumb-level">Niveau 1: Operator</span>
          <span class="bi-crumb-name">🚆 ${{h.level_1_operator.naam}}</span>
        </div>
        <span class="bi-crumb-arrow">➔</span>
        <div class="bi-crumb-card" onclick="openMasterDataModal('regio')">
          <span class="bi-crumb-level">Niveau 2: Regio</span>
          <span class="bi-crumb-name">🗺️ ${{h.level_2_regio.naam}}</span>
        </div>
        <span class="bi-crumb-arrow">➔</span>
        <div class="bi-crumb-card" onclick="openMasterDataModal('zone')">
          <span class="bi-crumb-level">Niveau 3: Zone</span>
          <span class="bi-crumb-name">⚓ ${{h.level_3_zone.naam}}</span>
        </div>
        <span class="bi-crumb-arrow">➔</span>
        <div class="bi-crumb-card" onclick="openMasterDataModal('moederbundel')">
          <span class="bi-crumb-level">Niveau 4: Moederbundel</span>
          <span class="bi-crumb-name">🟡 ${{h.level_4_moederbundel.naam}}</span>
        </div>
        <span class="bi-crumb-arrow">➔</span>
        <div class="bi-crumb-card" style="border-color:#3b82f6; background:rgba(37,99,235,0.15);">
          <span class="bi-crumb-level" style="color:#60a5fa;">Niveau 5: Terminal</span>
          <span class="bi-crumb-name" style="color:#93c5fd;">⭐ ${{h.level_5_terminal.naam}}</span>
        </div>
      `;

      // 2. Build Running Header HTML
      const runningHeaderHtml = `
        <div class="bi-running-header">
          <div class="bi-running-header-left">
            ${{ASSET_DB_LOGO ? `<img src="${{ASSET_DB_LOGO}}" style="height:18px; vertical-align:middle;" alt="DB Cargo">` : `<span style="background:#dc2626; color:#fff; padding:2px 5px; font-weight:900; border-radius:2px;">DB</span>`}}
            <span>DB Cargo Belgium</span>
          </div>
          <div>Bedieningsinstructie ${{bi.metadata.terminal_naam}} (Versie ${{bi.metadata.huidige_versie}})</div>
        </div>
      `;

      // 3. Assemble Exact Word Tables
      // Table 1: Identificatie
      const table1Html = `
        <table class="bi-word-table">
          <tbody>
            <tr>
              <td class="bg-grey" style="width: 28%;">Documentcode</td>
              <td>${{bi.metadata.documentcode}}</td>
            </tr>
            <tr>
              <td class="bg-grey">Auteur(s)</td>
              <td>${{bi.metadata.auteurs}}</td>
            </tr>
            <tr>
              <td class="bg-grey">Bron</td>
              <td>${{bi.metadata.bron_referentie}}</td>
            </tr>
            <tr>
              <td class="bg-grey">Handtekening</td>
              <td>Digitaal gevalideerd conform autorisatieprocedure</td>
            </tr>
          </tbody>
        </table>
      `;

      // Table 2: Autorisatie
      const table2Html = `
        <table class="bi-word-table">
          <tbody>
            <tr>
              <td colspan="2" class="bg-grey" style="text-align:center;">AUTORISATIE</td>
            </tr>
            <tr>
              <td style="width: 28%;">Functionaris</td>
              <td><strong>${{bi.metadata.autorisatie_functionaris}}</strong></td>
            </tr>
            <tr>
              <td>Ingangsdatum</td>
              <td>${{bi.metadata.autorisatie_ingangsdatum}}</td>
            </tr>
            <tr>
              <td>Goedkeuring</td>
              <td>${{bi.metadata.goedkeuring_systeem}}</td>
            </tr>
          </tbody>
        </table>
      `;

      // Table 3: Versiehistoriek
      const table3Html = `
        <table class="bi-word-table">
          <thead>
            <tr>
              <th style="width: 110px;">Datum</th>
              <th style="width: 80px;">Versie</th>
              <th>Wijziging & Autorisatie</th>
            </tr>
          </thead>
          <tbody>
            ${{(bi.versiebeheer || []).slice().reverse().map(v => `
              <tr>
                <td>${{v.datum}}</td>
                <td><strong>${{v.versie}}</strong></td>
                <td>${{v.wijziging}}</td>
              </tr>
            `).join('')}}
          </tbody>
        </table>
      `;

      // Table 4: Contactpersonen Real-time (Hierarchically filtered and dynamically rendered)
      const opContacts = (bi.contactpersonen.realtime || []).filter(c => c.niveau && c.niveau.includes('Operator'));
      const zoneContacts = (bi.contactpersonen.realtime || []).filter(c => c.niveau && (c.niveau.includes('Seinhuis') || c.niveau.includes('Dispatch') || c.niveau.includes('Haven')));
      const termContacts = (bi.contactpersonen.realtime || []).filter(c => c.niveau && c.niveau.includes('Terminal'));

      const table4Html = `
        <table class="bi-word-table">
          <tbody>
            <tr>
              <td colspan="3" class="header-group">DB Cargo Belgium (Operator)</td>
            </tr>
            ${{opContacts.map(c => `
              <tr>
                <td class="bi-bar-red"></td>
                <td style="width: 45%;">${{c.dienst}} ${{c.rol ? `(${{c.rol}})` : ''}}</td>
                <td><strong>${{c.telefoon}}</strong></td>
              </tr>
            `).join('')}}

            <tr>
              <td colspan="3" class="header-group">Infrabel Seinhuis & Lokale Opvolging (${{bi.hierarchie_levels.level_3_zone.seinhuis || bi.hierarchie_levels.level_3_zone.naam}})</td>
            </tr>
            ${{zoneContacts.map(c => `
              <tr>
                <td class="bi-bar-blue"></td>
                <td style="width: 45%;">${{c.dienst}} ${{c.rol ? `(${{c.rol}})` : ''}}</td>
                <td>${{c.telefoon && c.telefoon.includes('@') ? c.telefoon : `<strong>${{c.telefoon}}</strong>`}}</td>
              </tr>
            `).join('')}}

            <tr>
              <td colspan="3" class="header-group">${{bi.metadata.terminal_naam}} (Terminal / Klant)</td>
            </tr>
            ${{termContacts.length > 0 ? termContacts.map(c => `
              <tr>
                <td class="bi-bar-grey"></td>
                <td style="width: 45%;">${{c.dienst}} ${{c.rol ? `(${{c.rol}})` : ''}}</td>
                <td><strong>${{c.telefoon}}</strong></td>
              </tr>
            `).join('') : `
              <tr>
                <td class="bi-bar-grey"></td>
                <td style="width: 45%;">Operationeel Toezicht / Klant</td>
                <td>Ter plaatse / via Dispatcher</td>
              </tr>
            `}}
          </tbody>
        </table>
      `;

      // Table 5: Noodgeval/Calamiteit (with Infrabel blue and Hulpdiensten red)
      const table5Html = `
        <table class="bi-word-table">
          <tbody>
            <tr>
              <td colspan="3" class="header-group">Infrabel Nooddiensten</td>
            </tr>
            <tr>
              <td class="bi-bar-blue"></td>
              <td style="width: 45%;">Rode Telefoon (Infrabel Noodcentrale)</td>
              <td><strong style="color:#c00000;">+32 2 525 91 40</strong></td>
            </tr>
            <tr>
              <td class="bi-bar-blue"></td>
              <td>Oranje Telefoon (RID Incidenten & Meldingen)</td>
              <td>+32 2 528 81 50</td>
            </tr>
            <tr>
              <td class="bi-bar-blue"></td>
              <td>Permanentie I-TO (Area North-West)</td>
              <td>+32 5 030 22 23</td>
            </tr>

            <tr>
              <td colspan="3" class="header-group">Hulpdiensten</td>
            </tr>
            <tr>
              <td class="bi-bar-emergency"></td>
              <td>Brandweer (Medische Hulp & Brand)</td>
              <td><strong style="color:#c00000;">112</strong></td>
            </tr>
            <tr>
              <td class="bi-bar-emergency"></td>
              <td>Politie / Spoorwegpolitie</td>
              <td><strong>101 of 112</strong></td>
            </tr>
          </tbody>
        </table>
      `;

      // Table 10: Bedieningstijden
      const table10Html = `
        <table class="bi-word-table">
          <tbody>
            <tr>
              <td class="bg-grey" style="width: 30%;">Plaatsen van wagens</td>
              <td>${{bi.plaatselijke_regelgeving.bedieningstijden || '24/7, niet gespecificeerd, op verzoek van de klant'}}</td>
            </tr>
            <tr>
              <td class="bg-grey">Uithalen van wagens</td>
              <td>${{bi.plaatselijke_regelgeving.bedieningstijden || '24/7, niet gespecificeerd, op verzoek van de klant'}}</td>
            </tr>
          </tbody>
        </table>
      `;

      // Table 12 & Table 13: Stappenplannen
      let stepTable12Html = '';
      if (bi.procedures && bi.procedures.procedure_1_toegang) {{
        stepTable12Html = `
          <table class="bi-step-table">
            <thead>
              <tr>
                <th style="width: 65px; text-align:center;">STAP</th>
                <th>Operationele Handeling & Veiligheidsvoorschrift</th>
              </tr>
            </thead>
            <tbody>
              ${{bi.procedures.procedure_1_toegang.map(s => `
                <tr>
                  <td class="bi-step-num-cell">${{s.stap}}</td>
                  <td>
                    <strong>${{s.titel}}</strong>: ${{s.beschrijving}}
                  </td>
                </tr>
              `).join('')}}
            </tbody>
          </table>
        `;
      }}

      let stepTable13Html = '';
      if (bi.procedures && bi.procedures.procedure_3_verlaten) {{
        stepTable13Html = `
          <table class="bi-step-table">
            <thead>
              <tr>
                <th style="width: 65px; text-align:center;">STAP</th>
                <th>Operationele Handeling & Veiligheidsvoorschrift</th>
              </tr>
            </thead>
            <tbody>
              ${{bi.procedures.procedure_3_verlaten.map(s => `
                <tr>
                  <td class="bi-step-num-cell">${{s.stap}}</td>
                  <td>
                    <strong>${{s.titel}}</strong>: ${{s.beschrijving}}
                  </td>
                </tr>
              `).join('')}}
            </tbody>
          </table>
        `;
      }}

      // Table for Procedure 2 (Rangeringen spoor 872)
      let stepTableProc2Html = '';
      if (bi.procedures && bi.procedures.procedure_2_rangering_spoor_872) {{
        stepTableProc2Html = `
          <table class="bi-step-table">
            <thead>
              <tr>
                <th style="width: 65px; text-align:center;">STAP</th>
                <th>Procedure voor Rangeringen van/naar de Terminal tot op Spoor 872</th>
              </tr>
            </thead>
            <tbody>
              ${{bi.procedures.procedure_2_rangering_spoor_872.map(s => `
                <tr>
                  <td class="bi-step-num-cell">${{s.stap}}</td>
                  <td>
                    <strong>${{s.titel}}</strong>: ${{s.beschrijving}}
                  </td>
                </tr>
              `).join('')}}
            </tbody>
          </table>
        `;
      }}

      // Inhoudstafel HTML
      const tocHtml = `
        <div class="bi-toc-list">
          <a class="bi-toc-item level-1" href="#sec1"><span>1  Doel en Identificatie document</span><span>4</span></a>
          <a class="bi-toc-item level-2" href="#sec1_1"><span>1.1  Doel</span><span>4</span></a>
          <a class="bi-toc-item level-2" href="#sec1_2"><span>1.2  Identificatie</span><span>4</span></a>
          <a class="bi-toc-item level-2" href="#sec1_3"><span>1.3  Gebruikersgroep</span><span>4</span></a>
          <a class="bi-toc-item level-2" href="#sec1_4"><span>1.4  Autorisatie van dit document</span><span>4</span></a>
          <a class="bi-toc-item level-1" href="#sec2"><span>2  Contactpersonen</span><span>5</span></a>
          <a class="bi-toc-item level-2" href="#sec2_1"><span>2.1  Real Time Beheer: Contactpersonen</span><span>5</span></a>
          <a class="bi-toc-item level-2" href="#sec2_2"><span>2.2  Noodgeval/Calamiteit: Contactpersonen</span><span>5</span></a>
          <a class="bi-toc-item level-1" href="#sec3"><span>3  Wat doen bij calamiteiten</span><span>6</span></a>
          <a class="bi-toc-item level-2" href="#sec3_1"><span>3.1  Ontsnappingsroutes</span><span>6</span></a>
          <a class="bi-toc-item level-2" href="#sec3_2"><span>3.2  Verzamelpunten</span><span>6</span></a>
          <a class="bi-toc-item level-1" href="#sec4"><span>4  Overzicht van de installaties</span><span>7</span></a>
          <a class="bi-toc-item level-2" href="#sec4_1"><span>4.1  Situering van de aansluiting "${{bi.metadata.terminal_naam}}"</span><span>7</span></a>
          <a class="bi-toc-item level-3" href="#sec4_1_1"><span>4.1.1  Overzicht</span><span>7</span></a>
          <a class="bi-toc-item level-3" href="#sec4_1_2"><span>4.1.2  Parkeergelegenheid & toegang</span><span>7</span></a>
          <a class="bi-toc-item level-2" href="#sec4_2"><span>4.2  Bundel ${{bi.installaties.moederbundel.naam}}</span><span>8</span></a>
          <a class="bi-toc-item level-2" href="#sec4_3"><span>4.3  Aansluiting ${{bi.metadata.terminal_naam}}</span><span>12</span></a>
          <a class="bi-toc-item level-3" href="#sec4_3_1"><span>4.3.1  Sporen op de aansluiting</span><span>12</span></a>
          <a class="bi-toc-item level-3" href="#sec4_3_2"><span>4.3.2  Richting van de auto’s op de trein</span><span>12</span></a>
          <a class="bi-toc-item level-3" href="#sec4_3_3"><span>4.3.3  Beveiliging van de aansluiting</span><span>12</span></a>
          <a class="bi-toc-item level-3" href="#sec4_3_4"><span>4.3.4  SSP</span><span>12</span></a>
          <a class="bi-toc-item level-1" href="#sec5"><span>5  Risico’s op deze site</span><span>13</span></a>
          <a class="bi-toc-item level-2" href="#sec5_1"><span>5.1  Bovenleidingsgrenzen</span><span>13</span></a>
          <a class="bi-toc-item level-2" href="#sec5_2"><span>5.2  Overwegen op het traject</span><span>13</span></a>
          <a class="bi-toc-item level-2" href="#sec5_3"><span>5.3  Stuitklamp ter beveiliging</span><span>13</span></a>
          <a class="bi-toc-item level-2" href="#sec5_4"><span>5.4  Aanwezigheid andere Spoorwegondernemingen (SO)</span><span>13</span></a>
          <a class="bi-toc-item level-1" href="#sec6"><span>6  Bijzonderheden</span><span>13</span></a>
          <a class="bi-toc-item level-1" href="#sec7"><span>7  Bedieningsinstructie</span><span>14</span></a>
          <a class="bi-toc-item level-2" href="#sec7_1"><span>7.1  Voorwaarden om deze bediening uit te voeren</span><span>14</span></a>
          <a class="bi-toc-item level-2" href="#sec7_2"><span>7.2  Bedieningstijden</span><span>14</span></a>
          <a class="bi-toc-item level-2" href="#sec7_3"><span>7.3  Plaatselijke regelgeving</span><span>15</span></a>
          <a class="bi-toc-item level-3" href="#sec7_3_1"><span>7.3.1  Toegelaten rangeringen</span><span>15</span></a>
          <a class="bi-toc-item level-3" href="#sec7_3_2"><span>7.3.2  Snelheden</span><span>15</span></a>
          <a class="bi-toc-item level-3" href="#sec7_3_3"><span>7.3.3  Immobilisatie</span><span>15</span></a>
          <a class="bi-toc-item level-3" href="#sec7_3_4"><span>7.3.4  Remproeven en technische controles</span><span>15</span></a>
          <a class="bi-toc-item level-2" href="#sec7_4"><span>7.4  Bedienen van ${{bi.metadata.terminal_naam}}</span><span>16</span></a>
          <a class="bi-toc-item level-3" href="#sec7_4_1"><span>7.4.1  Een rit aanvragen van bundel naar aansluiting</span><span>16</span></a>
          <a class="bi-toc-item level-3" href="#sec7_4_2"><span>7.4.2  Rit naar de aansluiting (Stappenplan)</span><span>16</span></a>
          <a class="bi-toc-item level-3" href="#sec7_4_3"><span>7.4.3  Plaatsen wagens op aansluiting</span><span>18</span></a>
          <a class="bi-toc-item level-3" href="#sec7_4_4"><span>7.4.4  Uithalen wagens of verlaten aansluiting (Stappenplan)</span><span>18</span></a>
          <a class="bi-toc-item level-1" href="#sec8"><span>8  Versiebeheer & Wijzigingenlogboek (Changelog)</span><span>19</span></a>
        </div>
      `;

      // Full Master Assembly of the Document Card
      container.innerHTML = `
        <!-- COVER PAGE -->
        <div class="bi-cover-page">
          <div class="bi-cover-top">
            ${{ASSET_DB_LOGO ? `<img src="${{ASSET_DB_LOGO}}" style="height:52px;" alt="DB Cargo">` : `<div style="background:#dc2626; color:#ffffff; font-weight:900; font-size:24px; padding:6px 14px;">DB</div>`}}
          </div>
          <div class="bi-cover-center">
            <h1>Bedieningsinstructie</h1>
            <h2>${{bi.metadata.terminal_naam}}</h2>
            <h3>${{bi.metadata.moederbundel_naam}}</h3>
          </div>
          <div class="bi-cover-bottom">
            <span>DB Cargo Belgium • Buitendienst Documentatie</span>
            <span>Versie ${{bi.metadata.huidige_versie}} (${{bi.metadata.versie_datum}})</span>
          </div>
        </div>

        <div class="bi-page-break"></div>

        ${{runningHeaderHtml}}

        <!-- INHOUDSTAFEL -->
        <h2 style="color: #4472c4; font-size: 16pt; font-weight: bold; border-bottom: 2px solid #4472c4; padding-bottom: 4px; margin-top: 10px; margin-bottom: 14px;">Inhoudstafel</h2>
        ${{tocHtml}}

        <div class="bi-page-break"></div>

        ${{runningHeaderHtml}}

        <!-- HOOFDSTUK 1 -->
        <div id="sec1">
          <h2 class="bi-h1">1  Doel en Identificatie document</h2>
          
          <div id="sec1_1">
            <h3 class="bi-h2">1.1  Doel</h3>
            <p class="bi-p">Het beschrijven van een uniforme en veilige werkwijze op de bediening van ${{bi.metadata.terminal_naam}} en omliggende bundelsporen.</p>
          </div>

          <div id="sec1_2">
            <h3 class="bi-h2">1.2  Identificatie</h3>
            ${{table1Html}}
          </div>

          <div id="sec1_3">
            <h3 class="bi-h2">1.3  Gebruikersgroep</h3>
            <p class="bi-p">${{bi.metadata.gebruikersgroep}}</p>
          </div>

          <div id="sec1_4">
            <h3 class="bi-h2">1.4  Autorisatie van dit document</h3>
            ${{table2Html}}
            <p class="bi-p" style="margin-top:14px;"><strong>Versiehistoriek & Wijzigingen:</strong></p>
            ${{table3Html}}
          </div>
        </div>

        <div class="bi-page-break"></div>

        ${{runningHeaderHtml}}

        <!-- HOOFDSTUK 2 -->
        <div id="sec2">
          <h2 class="bi-h1">2  Contactpersonen</h2>
          
          <div id="sec2_1">
            <h3 class="bi-h2">2.1  Real Time Beheer: Contactpersonen</h3>
            <p class="bi-p">Onderstaande tabel toont de bevoegde operationele contactpersonen over de diverse niveaus:</p>
            ${{table4Html}}
          </div>

          <div id="sec2_2">
            <h3 class="bi-h2">2.2  Noodgeval/Calamiteit: Contactpersonen</h3>
            <p class="bi-p">In geval van een calamiteit, incident of gevaarlijke situatie dienen onderstaande diensten onmiddellijk gecontacteerd te worden:</p>
            ${{table5Html}}
          </div>
        </div>

        <div class="bi-page-break"></div>

        ${{runningHeaderHtml}}

        <!-- HOOFDSTUK 3 -->
        <div id="sec3">
          <h2 class="bi-h1">3  Wat doen bij calamiteiten</h2>
          
          <div id="sec3_1">
            <h3 class="bi-h2">3.1  Ontsnappingsroutes</h3>
            <p class="bi-p">Op de terminal ${{bi.metadata.terminal_naam}} zijn er geen specifieke gemarkeerde ontsnappingsroutes aangeduid. Bij nood verlaat men het spoor via de breedste veilige zijde weg van het spoorverkeer.</p>
          </div>

          <div id="sec3_2">
            <h3 class="bi-h2">3.2  Verzamelpunten</h3>
            <p class="bi-p">In geval van calamiteiten worden de aanwezige medewerkers verzameld op verzamelpunten aangeduid met onderstaand pictogram.</p>
            
            <div style="margin: 14px 0; text-align: center;">
              ${{ASSET_VERZAMELPUNT ? `<img src="${{ASSET_VERZAMELPUNT}}" style="height:85px;" alt="Verzamelpunt Pictogram">` : `<div style="display:inline-block; background:#059669; color:#fff; font-weight:bold; padding:12px 18px; border-radius:6px;">VERZAMELPUNT</div>`}}
            </div>

            <p class="bi-p">Wanneer er zich een incident voordoet, zal de aanwezige 24/7-security ambtshalve een “sweep” doen op de kaai om de aanwezige externen te verzamelen en te begeleiden naar de verzamelpunten.</p>
            <p class="bi-p">Elke persoon die op de terminal binnenkomt, ook via de spoorpoort, wordt geregistreerd. De medewerkers van de beveiliging weten dan ook altijd wie op de terminal aanwezig is.</p>
          </div>
        </div>

        <div class="bi-page-break"></div>

        ${{runningHeaderHtml}}

        <!-- HOOFDSTUK 4 -->
        <div id="sec4">
          <h2 class="bi-h1">4  Overzicht van de installaties</h2>

          <div id="sec4_1">
            <h3 class="bi-h2">4.1  Situering van de aansluiting "${{bi.metadata.terminal_naam}}"</h3>
            <div id="sec4_1_1">
              <h4 class="bi-h3">4.1.1  Overzicht</h4>
              <p class="bi-p">Het toepassingsgebied van deze instructie omvat de spoorlijnen rond ${{bi.hierarchie_levels.level_3_zone.naam}}, bundel ${{bi.installaties.moederbundel.naam}} en de private aansluiting ${{bi.metadata.terminal_naam}}.</p>
              <table class="bi-word-table">
                <tbody>
                  <tr>
                    <td class="bg-grey" style="width: 25%;">Bereikbaarheid Trein</td>
                    <td>${{bi.installaties.situering.bereikbaarheid.trein}}</td>
                  </tr>
                  <tr>
                    <td class="bg-grey">Bereikbaarheid Auto</td>
                    <td>${{bi.installaties.situering.bereikbaarheid.auto}} (${{bi.installaties.situering.adres}})</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div id="sec4_1_2">
              <h4 class="bi-h3">4.1.2  Parkeergelegenheid & toegang</h4>
              <p class="bi-p">Aan bundel ${{bi.installaties.moederbundel.naam}} is er voldoende gelegenheid tot parkeren:</p>
              <ul style="padding-left: 22px; font-size: 10pt; line-height: 1.5; margin-bottom: 12px;">
                ${{(bi.installaties.moederbundel.parkeergelegenheid || ['Parkeergelegenheid langs de bundel / spoorzone', 'Toegankelijk via openbare weg']).map(p => `<li>${{p}}</li>`).join('')}}
              </ul>
            </div>
          </div>

          <div id="sec4_2">
            <h3 class="bi-h2">4.2  ${{bi.installaties.moederbundel.naam}}</h3>
            <p class="bi-p"><strong>Beschrijving van de installaties:</strong></p>
            <ul style="padding-left: 22px; font-size: 10pt; line-height: 1.5; margin-bottom: 10px;">
              <li>${{bi.installaties.moederbundel.beseind ? 'Is een beseinde bundel uitgerust met seinen' : 'Niet-beseinde bundel / exploitatie goederensporen'}} (${{bi.installaties.moederbundel.seinen_info || 'seininrichting Infrabel'}});</li>
              <li>Bevat sporen met bovenleiding (${{bi.installaties.moederbundel.bovenleiding_info || 'Geëlektrificeerd'}});</li>
              <li>Is voorzien van tankinstallatie: ${{bi.installaties.moederbundel.tankinstallatie || 'Geen eigen installatie'}};</li>
              <li>Camerabewaking & toezicht: ${{bi.installaties.moederbundel.cameras || 'Toezicht Infrabel'}}.</li>
            </ul>

            ${{terminalId === 'cro_brit' ? `
              <p class="bi-p"><strong>Weetje lengte sporen:</strong></p>
              <p class="bi-p">Bundel Ramskapelle bestaat uit 8 lange sporen (881 t.e.m. 888) en 7 korte sporen (889 t.e.m. 895) om treinen te ontvangen en af te stellen.</p>

              <p class="bi-p"><strong>Schuifrangering kant Brugge:</strong></p>
              <p class="bi-p">Op lijn 202B is de mogelijkheid voorzien tot een schuifrangering tussen de sporen 857 en 858. Deze schuifrangering maakt het mogelijk om bij een rangering met terugrit naar de bundel met een stel langer dan 150m (locomotief inbegrepen) het sein KC-R.7 open te zetten, zodat de reisweg tussen de bundel en sein IC-R.7 kan worden vrijgemaakt.</p>
            ` : `
              <p class="bi-p"><strong>Schuif- en rangeerbewegingen:</strong></p>
              <p class="bi-p">${{bi.installaties.moederbundel.schuifrangering || `Rangeringen conform instructies van ${{bi.hierarchie_levels.level_3_zone.seinhuis}}.`}}</p>
            `}}
          </div>

          <div id="sec4_3">
            <h3 class="bi-h2">4.3  Aansluiting ${{bi.metadata.terminal_naam}}</h3>
            
            <div id="sec4_3_1">
              <h4 class="bi-h3">4.3.1  Sporen op de aansluiting</h4>
              ${{terminalId === 'cro_brit' ? `
                <p class="bi-p">Er bevinden zich 8 operationele sporen op de aansluiting (genummerd van links naar rechts bij binnenrijden):</p>
                <ul style="padding-left: 22px; font-size: 10pt; line-height: 1.5; margin-bottom: 10px;">
                  <li>Spoor 1 & 2: voorzien voor containers (lengte 520m)</li>
                  <li>Spoor 3 & 4: voorzien voor containers (lengte 565m)</li>
                  <li>Spoor 5 & 6: voorzien voor automotive / auto's (lengte 315m)</li>
                  <li>Spoor 7: voorzien voor automotive (lengte 372m)</li>
                  <li>Spoor 8: voorzien voor automotive (lengte 424m)</li>
                </ul>
              ` : `
                <p class="bi-p"><strong>Toegangsspoor:</strong> ${{infra.toegangsspoor || `Toegang vanaf ${{bi.installaties.moederbundel.naam}}`}}</p>
                <p class="bi-p"><strong>Bedieningssporen:</strong> ${{infra.terminal_sporen || 'Bedienings- en laadsporen ter plaatse'}}</p>
                <p class="bi-p"><strong>Laad- en loskade:</strong> ${{infra.laadkade || 'Bedieningssporen'}}</p>
              `}}
            </div>

            ${{terminalId === 'cro_brit' ? `
              <div id="sec4_3_2">
                <h4 class="bi-h3">4.3.2  Richting van de auto’s op de trein</h4>
                <div class="bi-word-callout">
                  <strong>RICHTING LADING:</strong> De neuzen van de auto’s op de trein dienen steeds gericht te zijn naar de <strong>ZEE (kust)</strong>. De koffers dienen steeds kant <strong>BRUGGE</strong> gericht te zijn bij binnenrijden/plaatsing.
                </div>
              </div>
            ` : (infra.richting_lading && infra.richting_lading !== 'NVT' && !infra.richting_lading.includes('dispatcher') ? `
              <div id="sec4_3_2">
                <h4 class="bi-h3">4.3.2  Richting van de lading</h4>
                <div class="bi-word-callout">
                  <strong>RICHTING LADING:</strong> ${{infra.richting_lading}}
                </div>
              </div>
            ` : '')}}

            <div id="sec4_3_3">
              <h4 class="bi-h3">4.3.3  Beveiliging van de aansluiting</h4>
              ${{terminalId === 'cro_brit' ? `
                <p class="bi-p">De aansluiting is beveiligd met een geslotteerde stuitklamp (stuitklamp 321) en een automatische spoorpoort. De sleutel (321) bevindt zich in de Siemensslotkast die is opgesteld nabij overweg 17 (afgesloten met Wilka G* sleutel).</p>
              ` : `
                <p class="bi-p">De aansluiting is beveiligd met: <strong>${{infra.beveiliging_infrabel || 'Handbediende wissels en/of stootjukken'}}</strong>.</p>
              `}}
            </div>

            <div id="sec4_3_4">
              <h4 class="bi-h3">4.3.4  SSP Referentie</h4>
              <p class="bi-p">De SSP is raadpleegbaar in <strong>${{bi.installaties.moederbundel.ssp_referentie || bi.metadata.bron_referentie}}</strong>.</p>
            </div>
          </div>
        </div>

        <div class="bi-page-break"></div>

        ${{runningHeaderHtml}}

        <!-- HOOFDSTUK 5 -->
        <div id="sec5">
          <h2 class="bi-h1">5  Risico’s op deze site</h2>
          ${{terminalId === 'cro_brit' ? `
            <div id="sec5_1">
              <h3 class="bi-h2">5.1  Spoor 844 lijn 202B is maar gedeeltelijk uitgerust met een bovenleiding</h3>
              <p class="bi-p">Het spoor 844 lijn 202B is maar over een lengte van 55m voorbij het terugritsein KD-R.7 uitgerust met een bovenleiding. Na aankomst van een trein in de bundel Ramskapelle wordt de elektrische locomotief via deze reisweg verspoord. Let strikt op het einde-bovenleidingsbord!</p>
            </div>

            <div id="sec5_2">
              <h3 class="bi-h2">5.2  Overwegen op het traject bundel Ramskapelle – CRO Brittaniadok</h3>
              <p class="bi-p">Er bevinden zich meerdere overwegen op het traject (o.a. OW15 en OW17). Het wegverkeer houdt niet altijd rekening met de lichtsignalisatie. De overweg 17, pal aan de poort van SEA-RO Brittaniadok, wordt intens gebruikt door vrachtwagens, fietsers en voetgangers; wees hier extra alert voor!</p>
            </div>

            <div id="sec5_3">
              <h3 class="bi-h2">5.3  Stuitklamp ter beveiliging van de aansluiting</h3>
              <p class="bi-p">De aansluiting wordt beveiligd door stuitklamp 321. Vergewis u er zich steeds van dat deze open ligt vóór elke overschrijding, onder elke omstandigheid.</p>
            </div>

            <div id="sec5_4">
              <h3 class="bi-h2">5.4  Aanwezigheid andere Spoorwegondernemingen (SO)</h3>
              <p class="bi-p">Op de site kunnen andere spoorwegondernemingen actief zijn. Deze kunnen onterecht een rangeerbeweging uitvoeren. Maximale waakzaamheid en radiocontact houden is verplicht.</p>
            </div>
          ` : `
            ${{(bi.veiligheid_en_risicos || []).filter(r => r.type !== 'Bedrijfsvoorschrift').map((r, idx) => `
              <div id="sec5_${{idx+1}}">
                <h3 class="bi-h2">5.${{idx+1}}  ${{r.type}}: ${{r.omschrijving.split(':')[0]}}</h3>
                <p class="bi-p">${{r.omschrijving.includes(':') ? r.omschrijving.split(':').slice(1).join(':').trim() : r.omschrijving}}</p>
                <p class="bi-p-small"><em>Geverifieerde bron: ${{r.bron}}</em></p>
              </div>
            `).join('') || `
              <div id="sec5_1">
                <h3 class="bi-h2">5.1  Specifieke risico's</h3>
                <p class="bi-p">Waakzaamheid geboden voor wisselbediening, spoorbezetting en stootjukken conform de plaatselijke instructies.</p>
              </div>
            `}}
          `}}
        </div>

        <div id="sec6" style="margin-top:20px;">
          <h2 class="bi-h1">6  Bijzonderheden</h2>
          <p class="bi-p">${{terminalId === 'cro_brit' ? 'Lijnkennis van L202B en havenlijnen Zeebrugge is te allen tijde vereist.' : `Lijnkennis van ${{bi.installaties.moederbundel.naam}} en actiezone ${{bi.hierarchie_levels.level_3_zone.naam}} is te allen tijde vereist.`}}</p>
        </div>

        <div class="bi-page-break"></div>

        ${{runningHeaderHtml}}

        <!-- HOOFDSTUK 7 -->
        <div id="sec7">
          <h2 class="bi-h1">7  Bedieningsinstructie</h2>

          <div id="sec7_1">
            <h3 class="bi-h2">7.1  Voorwaarden om deze bediening uit te voeren</h3>
            
            <p class="bi-p"><strong>Treinbestuurder:</strong></p>
            <ul style="padding-left: 22px; font-size: 9.5pt; line-height: 1.45; margin-bottom: 8px;">
              <li>Geldig Aanvullend Bevoegdheidsbewijs (AB) DB Cargo Belgium;</li>
              <li>Kennis van deze bediening en deze bedieningsinstructie;</li>
              <li>PBM’s: Veiligheidshelm, handschoenen, gele fluo veiligheidskledij, gehoorbescherming en veiligheidsschoenen S3;</li>
              <li>De nodige lijnkennis vermeld op het aanvullend bevoegdheidsbewijs;</li>
              <li>Certificaat “${{bi.hierarchie_levels.level_3_zone.naam}} – ${{bi.metadata.terminal_naam}}” in RailCube.</li>
            </ul>

            <p class="bi-p"><strong>Schouwer / Rangeerder:</strong></p>
            <ul style="padding-left: 22px; font-size: 9.5pt; line-height: 1.45; margin-bottom: 8px;">
              <li>Geldig attest DB Cargo Belgium;</li>
              <li>Kennis van deze bediening en bedieningsinstructie;</li>
              <li>PBM’s: Veiligheidshelm, handschoenen, gele fluo veiligheidskledij, gehoorbescherming & veiligheidsschoenen S3;</li>
              <li>Certificaat “${{bi.hierarchie_levels.level_3_zone.naam}} – ${{bi.metadata.terminal_naam}}” in RailCube.</li>
            </ul>

            <p class="bi-p"><strong>Hulponderneming:</strong></p>
            <ul style="padding-left: 22px; font-size: 9.5pt; line-height: 1.45; margin-bottom: 8px;">
              <li>Geldig attest en toelating DB Cargo Belgium;</li>
              <li>Kennis van deze bediening / instructie;</li>
              <li>Voorgeschreven PBM’s en RailCube kwalificatie.</li>
            </ul>
          </div>

          <div id="sec7_2">
            <h3 class="bi-h2">7.2  Bedieningstijden</h3>
            ${{table10Html}}
          </div>

          <div id="sec7_3">
            <h3 class="bi-h2">7.3  Plaatselijke regelgeving</h3>
            
            <div id="sec7_3_1">
              <h4 class="bi-h3">7.3.1  Toegelaten rangeringen</h4>
              <p class="bi-p">Enkel de “Gewone rangering” is toegelaten (= opgeduwde of getrokken beweging in kleine beweging).</p>
            </div>

            <div id="sec7_3_2">
              <h4 class="bi-h3">7.3.2  Snelheden</h4>
              <p class="bi-p">De maximumsnelheid op heel de site bedraagt <strong>5 km/h</strong>, zowel voor een getrokken als opgeduwde beweging.</p>
            </div>

            <div id="sec7_3_3">
              <h4 class="bi-h3">7.3.3  Immobilisatie</h4>
              <p class="bi-p">Stellen moeten geïmmobiliseerd worden door middel van schroefremmen. In alle omstandigheden is een rempercentage van 2% vereist voor het immobiliseren van voertuigen.</p>
              <div class="bi-word-callout">
                <strong>🌪️ STORMWEER REGLEMENTERING:</strong> Indien er stormweer actief is of aangekondigd wordt, dient men rekening te houden met een minimum hellingswaarde van <strong>6 ‰</strong> voor het berekenen van de immobilisatiekracht. Bijkomend moet er nagekeken worden of alle voertuigen onderling met elkaar gekoppeld zijn. Het gebruik van stopblokken is <strong>STRIKT VERBODEN</strong>.
              </div>
            </div>

            <div id="sec7_3_4">
              <h4 class="bi-h3">7.3.4  Remproeven en technische controles</h4>
              <p class="bi-p">Technische controle, remproeven en onderzoek van wagens en lading mag enkel worden uitgevoerd door een bevoegde schouwer/rangeerder in het bezit van een geldig attest. Remproeven mogen ook door de bestuurder alleen uitgevoerd worden bij afwezigheid van ander personeel.</p>
            </div>
          </div>

          <div id="sec7_4">
            <h3 class="bi-h2">7.4  Bedienen van ${{bi.metadata.terminal_naam}}</h3>

            <div id="sec7_4_1">
              <h4 class="bi-h3">7.4.1  Een rit aanvragen van ${{bi.metadata.moederbundel_naam}} naar ${{bi.metadata.terminal_naam}}</h4>
              ${{terminalId === 'cro_brit' ? `
                <p class="bi-p">De rit naar CRO Brittaniadok dient aangevraagd te worden bij Infrabel Blok 7. Om een beweging vanuit bundel Ramskapelle naar CRO te kunnen toelaten:</p>
                <ul style="padding-left: 22px; font-size: 9.5pt; line-height: 1.45; margin-bottom: 6px;">
                  <li>Dienen ze te beschikken over het slot 321FR;</li>
                  <li>Mogen er geen rangeringen meer plaatsvinden op het spoor 872;</li>
                  <li>Tijdens rangeringen zijn ritten naar Ramskapelle strikt verboden!</li>
                </ul>
                <p class="bi-p">Dit om te vermijden dat er treinen kop-aan-kop komen te staan t.h.v. de seinen MD-R.7 en ND-R.7.</p>
              ` : `
                <p class="bi-p">De bedieningsrit naar ${{bi.metadata.terminal_naam}} dient te worden aangevraagd bij <strong>${{bi.hierarchie_levels.level_3_zone.seinhuis}}</strong>. Vergewis je van de toelating, de actuele spoorbezetting en de reisweg alvorens de beweging aan te vatten.</p>
              `}}
            </div>

            <div id="sec7_4_2">
              <h4 class="bi-h3">7.4.2  Rit naar ${{bi.metadata.terminal_naam}} (Aanvoer / Toegang)</h4>
              ${{stepTable12Html}}
            </div>

            <div id="sec7_4_3">
              <h4 class="bi-h3">7.4.3  Plaatsen wagens op ${{bi.metadata.terminal_naam}}</h4>
              ${{terminalId === 'cro_brit' ? `
                <p class="bi-p">Het plaatsen van wagens gebeurt als opduwen van bundel Ramskapelle naar de bediening CRO. Controleer stand autolichten (kant kust).</p>
              ` : `
                <p class="bi-p">Het plaatsen van de wagens gebeurt als bedieningsbeweging vanuit ${{bi.metadata.moederbundel_naam}} naar de bedieningssporen van ${{bi.metadata.terminal_naam}}. Controleer steeds de immobilisatie (schroefremmen/spieën) en het vrijsignalisatiepunt.</p>
              `}}
            </div>

            ${{stepTableProc2Html ? `
              <div id="sec7_4_2b" style="margin-top:14px;">
                <h4 class="bi-h3">7.4.3b  Rangeringen van/naar de Terminal tot op spoor 872</h4>
                ${{stepTableProc2Html}}
              </div>
            ` : ''}}

            <div id="sec7_4_4" style="margin-top:14px;">
              <h4 class="bi-h3">7.4.4  Uithalen wagens of verlaten van ${{bi.metadata.terminal_naam}} (Afvoer)</h4>
              ${{terminalId === 'cro_brit' ? `
                <p class="bi-p">Let bij het uithalen van een trein op volgende zaken: aangebrachte ketting aan het stootjuk; vaste handremmen losmaken.</p>
              ` : `
                <p class="bi-p">Controleer vóór vertrek of alle immobilisatiemiddelen verwijderd zijn, de koppeling en remleiding in orde zijn en vraag de vertrektoelating aan bij <strong>${{bi.hierarchie_levels.level_3_zone.seinhuis}}</strong>.</p>
              `}}
              ${{stepTable13Html}}
            </div>
          </div>
        </div>

        <div class="bi-page-break"></div>

        ${{runningHeaderHtml}}

        <!-- HOOFDSTUK 8 -->
        <div id="sec8">
          <h2 class="bi-h1">8  Versiebeheer & Wijzigingenlogboek (Changelog)</h2>
          <p class="bi-p">Onderstaand overzicht bevat de volledige traceerbare versiehistoriek van deze instructie. Bij elke nieuwe generatie of update worden de wijzigingen automatisch geregistreerd:</p>
          ${{table3Html}}
        </div>
      `;
    }}

    // Modal: Nieuwe Versie Genereren
    function openNewVersionModal() {{
      const bi = getResolvedBiForTerminal(currentSelectedBiTerminalId);
      if (!bi) return;

      const modal = document.getElementById('newVersionModal');
      const intro = document.getElementById('newVersionModalIntro');
      const verInput = document.getElementById('newVersionNumberInput');
      const dateInput = document.getElementById('newVersionDateInput');
      const authorInput = document.getElementById('newVersionAuthorInput');
      const changelogInput = document.getElementById('newVersionChangelogInput');

      intro.innerHTML = `Genereer een nieuwe officiële versie van de Bedieningsinstructie voor <strong>${{bi.metadata.terminal_naam}}</strong> (huidige versie is v${{bi.metadata.huidige_versie}}).`;

      const currentVerNum = parseFloat(bi.metadata.huidige_versie) || 1.0;
      verInput.value = (currentVerNum + 0.1).toFixed(1);

      const now = new Date();
      dateInput.value = now.toISOString().split('T')[0];

      changelogInput.value = '';
      modal.classList.add('active');
    }}

    function closeNewVersionModal() {{
      const modal = document.getElementById('newVersionModal');
      if (modal) modal.classList.remove('active');
    }}

    function submitNewBiVersion() {{
      const verInput = document.getElementById('newVersionNumberInput');
      const dateInput = document.getElementById('newVersionDateInput');
      const authorInput = document.getElementById('newVersionAuthorInput');
      const changelogInput = document.getElementById('newVersionChangelogInput');

      const newVer = (verInput.value || '').trim();
      const newDate = (dateInput.value || '').trim();
      const newAuthor = (authorInput.value || '').trim();
      const newChanges = (changelogInput.value || '').trim();

      if (!newVer || !newChanges) {{
        alert('Vul a.u.b. een versienummer en een omschrijving van de wijzigingen (changelog) in.');
        return;
      }}

      let formattedDate = newDate;
      if (newDate.includes('-')) {{
        const parts = newDate.split('-');
        if (parts.length === 3 && parts[0].length === 4) {{
          formattedDate = `${{parts[2]}}-${{parts[1]}}-${{parts[0]}}`;
        }}
      }}

      const termId = currentSelectedBiTerminalId;
      const bi = getResolvedBiForTerminal(termId);

      let versions = bi.versiebeheer ? JSON.parse(JSON.stringify(bi.versiebeheer)) : [];
      versions.push({{
        "versie": newVer,
        "datum": formattedDate,
        "wijziging": newChanges
      }});

      customVersionsStore[termId] = {{
        "huidige_versie": newVer,
        "versie_datum": formattedDate,
        "auteurs": newAuthor,
        "versiebeheer": versions
      }};

      try {{
        localStorage.setItem(STORAGE_CUSTOM_BI_VERSIONS_KEY, JSON.stringify(customVersionsStore));
      }} catch(e) {{}}

      closeNewVersionModal();
      renderBiDocument(termId);
      showToast(`✓ Versie v${{newVer}} succesvol gegenereerd en geregistreerd in het changelog!`, 'success');
    }}

    // Print Document / PDF Trigger
    function printBiDocument() {{
      window.print();
    }}

    // Modal: Master Data Inspection (Levels 1 to 4)
    function openMasterDataModal(levelKey) {{
      const modal = document.getElementById('masterDataModal');
      const title = document.getElementById('masterDataModalTitle');
      const body = document.getElementById('masterDataModalBody');

      let contentHtml = '';

      if (levelKey === 'operator' || !levelKey) {{
        const op = rawHierarchicalLevels.operator;
        title.innerHTML = `🏢 Niveau 1: Bedrijf / Operator (${{op.naam}})`;
        contentHtml = `
          <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid #334155; margin-bottom:14px;">
            <p><strong>Doel:</strong> ${{op.doel}}</p>
            <p style="margin-top:6px;"><strong>Autorisatie:</strong> ${{op.autorisatie_functionaris}} (${{op.goedkeuring_systeem}})</p>
            <p style="margin-top:6px;"><strong>Gebruikersgroep:</strong> ${{op.gebruikersgroep}}</p>
          </div>
          <h4 style="color:#38bdf8; font-size:13px; font-weight:800; margin: 10px 0;">Algemene Bedrijfsvoorschriften (Cascaderen naar ELKE BI):</h4>
          <ul style="padding-left:20px; line-height:1.6; color:#cbd5e1; font-size:13px;">
            ${{op.algemene_veiligheidsregels.map(r => `<li>${{r}}</li>`).join('')}}
          </ul>
          <h4 style="color:#ef4444; font-size:13px; font-weight:800; margin: 14px 0 6px 0;">Landelijke Noodcentrales & Dispatch:</h4>
          <table class="bi-table">
            <thead><tr><th>Dienst</th><th>Rol</th><th>Nummer</th></tr></thead>
            <tbody>
              ${{op.noodcontacten.map(n => `<tr><td><strong>${{n.dienst}}</strong></td><td>${{n.rol}}</td><td><code>${{n.telefoon}}</code></td></tr>`).join('')}}
            </tbody>
          </table>
        `;
      }} else if (levelKey === 'regio') {{
        const reg = rawHierarchicalLevels.regio.west_vlaanderen;
        title.innerHTML = `🗺️ Niveau 2: Regio (${{reg.naam}})`;
        contentHtml = `
          <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid #334155; margin-bottom:14px;">
            <p><strong>Infrabel District:</strong> ${{reg.infrabel_district}}</p>
            <p style="margin-top:6px;"><strong>Permanentie I-TO:</strong> ${{reg.permanentie_ito}}</p>
            <p style="margin-top:6px;"><strong>Traffic Officer Area NW:</strong> ${{reg.traffic_officer_nw}}</p>
            <p style="margin-top:6px;"><strong>SSP Zone:</strong> ${{reg.ssp_zone}}</p>
          </div>
          <p style="font-size:13px; color:#94a3b8; line-height:1.5;">Regio-gegevens garanderen dat bij incidenten in West-Vlaanderen onmiddellijk contact wordt opgenomen met de bevoegde Traffic Officer en Permanentie I-TO van Area North-West.</p>
        `;
      }} else if (levelKey === 'zone') {{
        const bi = getResolvedBiForTerminal(currentSelectedBiTerminalId);
        const zId = bi.hierarchie_levels.level_3_zone.code || 'zeebrugge';
        const z = rawHierarchicalLevels.zones[zId] || rawHierarchicalLevels.zones['zeebrugge'];
        title.innerHTML = `⚓ Niveau 3: Zone / Hub (${{z.naam}})`;
        contentHtml = `
          <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid #334155; margin-bottom:14px;">
            <p><strong>Centraal Seinhuis:</strong> ${{z.centraal_seinhuis}}</p>
            ${{z.havenautoriteit ? `<p style="margin-top:6px;"><strong>Havenkapiteinsdienst:</strong> ${{z.havenautoriteit.naam}} (${{z.havenautoriteit.telefoon}}) • VHF: ${{z.havenautoriteit.vhf_kanalen}}</p>` : ''}}
          </div>
          <h4 style="color:#38bdf8; font-size:13px; font-weight:800; margin:10px 0;">Seinhuis Contactpersonen:</h4>
          <table class="bi-table">
            <thead><tr><th>Functie</th><th>Rol</th><th>Contact</th></tr></thead>
            <tbody>
              ${{z.seinhuis_contacten.map(c => `<tr><td><strong>${{c.dienst}}</strong></td><td>${{c.rol}}</td><td><code>${{c.telefoon}}</code></td></tr>`).join('')}}
            </tbody>
          </table>
          <h4 style="color:#f59e0b; font-size:13px; font-weight:800; margin:14px 0 6px 0;">Specifieke Zonerisico's:</h4>
          <ul style="padding-left:20px; line-height:1.6; color:#cbd5e1; font-size:13px;">
            ${{z.zone_risicos.map(r => `<li>${{r}}</li>`).join('')}}
          </ul>
        `;
      }} else if (levelKey === 'moederbundel') {{
        const bi = getResolvedBiForTerminal(currentSelectedBiTerminalId);
        const mbId = bi.hierarchie_levels.level_4_moederbundel.code || 'ramskapelle';
        const mb = rawHierarchicalLevels.moederbundels[mbId] || rawHierarchicalLevels.moederbundels['ramskapelle'];
        title.innerHTML = `🟡 Niveau 4: Moederbundel (${{mb.naam}})`;
        contentHtml = `
          <div style="background:#1e293b; padding:14px; border-radius:8px; border:1px solid #334155; margin-bottom:14px;">
            <p><strong>Infrabel PPGI Referentie:</strong> ${{mb.ppgi_referentie}}</p>
            <p style="margin-top:6px;"><strong>SSP Referentie:</strong> ${{mb.ssp_referentie}}</p>
            <p style="margin-top:6px;"><strong>Beseind:</strong> ${{mb.beseind ? 'Ja (met stopseinen en dwergseinen)' : 'Nee'}}</p>
            <p style="margin-top:6px;"><strong>Bovenleiding:</strong> ${{mb.bovenleiding_info}}</p>
            <p style="margin-top:6px;"><strong>Tankinstallatie:</strong> ${{mb.tankinstallatie}}</p>
            <p style="margin-top:6px;"><strong>Cameratoezicht:</strong> ${{mb.cameras}}</p>
          </div>
          ${{mb.bundel_sporen && mb.bundel_sporen.length > 0 ? `
            <h4 style="color:#38bdf8; font-size:13px; font-weight:800; margin:10px 0;">Bundelsporen & Beveiliging:</h4>
            <table class="bi-table">
              <thead><tr><th>Spoor</th><th>Type</th><th>Beveiliging</th></tr></thead>
              <tbody>
                ${{mb.bundel_sporen.map(s => `<tr><td><strong>${{s.spoor}}</strong></td><td>${{s.type}}</td><td><code>${{s.beveiliging}}</code></td></tr>`).join('')}}
              </tbody>
            </table>
          ` : ''}}
        `;
      }}

      body.innerHTML = contentHtml;
      modal.classList.add('active');
    }}

    function closeMasterDataModal() {{
      const modal = document.getElementById('masterDataModal');
      if (modal) modal.classList.remove('active');
    }}

    // ========================================================
    // PPGI AUDIT REVIEW PROPOSALS RENDERER
    // ========================================================
    function renderPpgiProposals() {{
      const container = document.getElementById('ppgiProposalsContainer');
      if (!container) return;

      let appliedCount = 0;
      let highCount = 0;
      let medCount = 0;

      rawPpgiProposals.forEach(p => {{
        if (appliedProposalsStore[p.id]) appliedCount++;
        if (p.urgentie === 'HOOG') highCount++;
        if (p.urgentie === 'MEDIUM') medCount++;
      }});

      const ppgiBadge = document.getElementById('ppgiBadgeCount');
      if (ppgiBadge) {{
        const remaining = rawPpgiProposals.length - appliedCount;
        ppgiBadge.textContent = remaining;
        ppgiBadge.style.display = remaining > 0 ? 'inline-block' : 'none';
      }}

      const mApplied = document.getElementById('ppgiMetricApplied');
      const mHigh = document.getElementById('ppgiMetricHigh');
      const mMed = document.getElementById('ppgiMetricMedium');
      if (mApplied) mApplied.textContent = appliedCount;
      if (mHigh) mHigh.textContent = highCount;
      if (mMed) mMed.textContent = medCount;

      container.innerHTML = rawPpgiProposals.map(prop => {{
        const isApplied = !!appliedProposalsStore[prop.id];
        return `
          <div class="ppgi-proposal-card urgency-${{prop.urgentie_badge}}">
            <div class="ppgi-card-header">
              <div class="ppgi-card-title-group">
                <span class="ppgi-prop-id">${{prop.id}}</span>
                <span class="ppgi-prop-title">${{prop.titel}}</span>
              </div>
              <span class="badge-urgency badge-urgency-${{prop.urgentie_badge}}">${{prop.urgentie}} URGENTIE</span>
            </div>

            <div class="ppgi-card-body">
              <div class="ppgi-ref-badge-row">
                <span>📄 Bron: <strong class="ppgi-ref-tag">${{prop.bron_document}}</strong></span>
                <span>📌 Sectie: <strong class="ppgi-ref-tag">${{prop.bron_sectie}}</strong></span>
                <span>🏛️ Toepassingsniveau: <strong class="ppgi-ref-tag" style="color:#38bdf8;">${{prop.niveau}}</strong></span>
              </div>

              <div class="ppgi-diff-grid">
                <div class="ppgi-diff-box ppgi-diff-current">
                  <div class="ppgi-diff-label">❌ Huidige situatie in BI (v2.2):</div>
                  <p>${{prop.huidige_waarde_bi}}</p>
                </div>
                <div class="ppgi-diff-box ppgi-diff-proposed">
                  <div class="ppgi-diff-label">✅ Voorgestelde aanpassing conform Infrabel PPGI:</div>
                  <p>${{prop.voorgestelde_waarde_ppgi}}</p>
                </div>
              </div>

              <div class="ppgi-rationale-box">
                <strong>💡 Motivering & Veiligheidsanalyse:</strong> ${{prop.motivering}}
              </div>
            </div>

            <div class="ppgi-card-footer">
              <span style="font-size:12px; color:#94a3b8;">
                Status: <strong>${{isApplied ? '✓ Reeds doorgevoerd in v2.3' : prop.status}}</strong>
              </span>

              ${{isApplied ? `
                <div class="btn-ppgi-applied">
                  <span>✓</span> Toegepast in BI (Zie Changelog)
                </div>
              ` : `
                <button class="btn-ppgi-apply" onclick="applyPpgiProposal('${{prop.id}}')">
                  <span>✓</span> Pas Voorstel Toe in BI
                </button>
              `}}
            </div>
          </div>
        `;
      }}).join('');
    }}

    function applyPpgiProposal(propId) {{
      const prop = rawPpgiProposals.find(p => p.id === propId);
      if (!prop) return;

      appliedProposalsStore[propId] = true;
      try {{
        localStorage.setItem(STORAGE_APPLIED_PROPOSALS_KEY, JSON.stringify(appliedProposalsStore));
      }} catch(e) {{}}

      const termId = 'cro_brit';
      const bi = getResolvedBiForTerminal(termId);
      let versions = bi.versiebeheer ? JSON.parse(JSON.stringify(bi.versiebeheer)) : [];
      
      const newVer = "2.3";
      const now = new Date();
      const formattedDate = `${{String(now.getDate()).padStart(2, '0')}}-${{String(now.getMonth() + 1).padStart(2, '0')}}-${{now.getFullYear()}}`;

      const changeMsg = `Inpassing PPGI wijziging (${{prop.id}}): ${{prop.titel}}. Bron: ${{prop.bron_document}}.`;
      if (!versions.some(v => v.wijziging.includes(prop.id))) {{
        versions.push({{
          "versie": newVer,
          "datum": formattedDate,
          "wijziging": changeMsg
        }});

        customVersionsStore[termId] = {{
          "huidige_versie": newVer,
          "versie_datum": formattedDate,
          "auteurs": "Bart VERCAEMPST Teamleader DBC.BE",
          "versiebeheer": versions
        }};
        try {{
          localStorage.setItem(STORAGE_CUSTOM_BI_VERSIONS_KEY, JSON.stringify(customVersionsStore));
        }} catch(e) {{}}
      }}

      renderPpgiProposals();
      showToast(`✓ Voorstel ${{prop.id}} succesvol toegepast! Schakel naar BI Generator om de wijziging te zien.`, 'success');
    }}
    '''
