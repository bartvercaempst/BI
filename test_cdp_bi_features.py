"""
Automated CDP test runner for BI Generator tabs & features.
"""

import asyncio
import json
import os
import subprocess
import time
import urllib.request
import websockets

async def run_cdp_tests():
    port = 9223
    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    file_url = r"file:///d:/Users/BKU/BartVercaempst/OneDrive - Deutsche Bahn/Documents/26-AI-Projecten/BI Generator/index.html"
    
    user_data = os.path.join(os.environ.get("TEMP", "C:\\TEMP"), "edge_test_profile_9223")
    cmd = [
        edge_path,
        "--headless=new",
        f"--remote-debugging-port={port}",
        f"--user-data-dir={user_data}",
        "--allow-file-access-from-files",
        "--disable-web-security",
        "--disable-gpu",
        "--no-first-run",
        file_url
    ]
    
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2.5)
    
    try:
        req = urllib.request.urlopen(f"http://127.0.0.1:{port}/json")
        tabs = json.loads(req.read().decode('utf-8'))
        target_tab = None
        for t in tabs:
            if "BI Generator" in t.get("title", ""):
                target_tab = t
                break
        
        if not target_tab:
            print("ERROR: BI Generator tab not found")
            return
        
        ws_url = target_tab["webSocketDebuggerUrl"]
        print("Connecting to CDP:", ws_url)
        
        async with websockets.connect(ws_url) as ws:
            msg_id = 1
            
            async def eval_js(expr):
                nonlocal msg_id
                req_obj = {
                    "id": msg_id,
                    "method": "Runtime.evaluate",
                    "params": {
                        "expression": expr,
                        "returnByValue": True
                    }
                }
                msg_id += 1
                await ws.send(json.dumps(req_obj))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get("id") == req_obj["id"]:
                        return resp.get("result", {}).get("result", {}).get("value")

            # Enable Runtime console events & check for errors
            await ws.send(json.dumps({"id": msg_id, "method": "Runtime.enable"}))
            msg_id += 1
            await ws.send(json.dumps({"id": msg_id, "method": "Log.enable"}))
            msg_id += 1

            # Give a moment for the page to initialize
            await asyncio.sleep(1)

            # Check if there was any exception
            chk = await eval_js("window.location.href")
            print("Current location:", chk)
            leaf = await eval_js("typeof L")
            print("typeof L:", leaf)
            err = await eval_js("typeof allItems !== 'undefined' ? allItems.length : 'allItems is undefined'")
            print("Status check:", err)

            # Test 1: Check basic variables
            num_locs = await eval_js("typeof allItems !== 'undefined' ? allItems.length : null")
            num_bedieningen = await eval_js("allItems.filter(x => !x.is_bundel).length")
            print(f"[TEST 1] allItems count: {num_locs} (48 total), Bedieningen count: {num_bedieningen} (39)")
            assert num_locs == 48 and num_bedieningen == 39

            # Test 2: Switch to BI Tab
            await eval_js("switchMainTab('bi')")
            active_tab = await eval_js("currentMainTab")
            print(f"[TEST 2] Active Main Tab: {active_tab} (expected 'bi')")
            assert active_tab == 'bi'

            # Test 3: Check BI Document Header for CRO Brittaniadok
            bi_title = await eval_js("document.querySelector('.bi-doc-title-box h1')?.innerText")
            print(f"[TEST 3] Rendered BI Title: {bi_title}")
            assert "BEDIENINGSINSTRUCTIE" in str(bi_title)

            # Test 4: Check Breadcrumbs
            crumbs_count = await eval_js("document.querySelectorAll('.bi-crumb-card').length")
            print(f"[TEST 4] Breadcrumb Level Count: {crumbs_count} (expected 5 levels)")
            assert crumbs_count == 5

            # Test 5: Check 8 chapters
            chapters_count = await eval_js("document.querySelectorAll('.bi-chapter').length")
            print(f"[TEST 5] Chapters rendered: {chapters_count} (expected 8 chapters)")
            assert chapters_count == 8

            # Test 6: Switch terminal to Wallenius Canadakaai (wal_can)
            await eval_js("onBiTerminalSelected('wal_can')")
            wal_title = await eval_js("document.querySelector('.bi-doc-title-box h1')?.innerText")
            print(f"[TEST 6] Switch to Wallenius Canadakaai Title: {wal_title}")
            assert "WALLENIUS" in str(wal_title) or "CAST" in str(wal_title)

            # Test 7: Switch to PPGI Tab & Check Proposals
            await eval_js("switchMainTab('ppgi')")
            num_props = await eval_js("document.querySelectorAll('.ppgi-proposal-card').length")
            print(f"[TEST 7] PPGI Proposal cards: {num_props} (expected 5)")
            assert num_props == 5

            # Test 8: Apply Proposal PROP-2026-001
            await eval_js("applyPpgiProposal('PROP-2026-001')")
            applied_badge = await eval_js("document.querySelector('.btn-ppgi-applied')?.innerText")
            clean_badge = str(applied_badge).encode('ascii', 'replace').decode('ascii')
            print(f"[TEST 8] Applied proposal badge: {clean_badge}")
            assert "Toegepast" in str(applied_badge)

            # Test 9: Verify CRO Brittaniadok received changelog entry v2.3
            await eval_js("switchMainTab('bi'); onBiTerminalSelected('cro_brit')")
            current_ver = await eval_js("document.querySelector('.bi-doc-version-pill strong')?.innerText")
            print(f"[TEST 9] CRO Brittaniadok new version: {current_ver} (expected v2.3)")
            assert "2.3" in str(current_ver)

            # Test 10: Switch back to Map Tab
            await eval_js("switchMainTab('map')")
            map_display = await eval_js("document.getElementById('mapView').style.display")
            print(f"[TEST 10] Map View Display style: {map_display} (expected 'flex')")
            assert map_display == 'flex'

            print("\n==========================================")
            print("ALL 10 BROWSER RUNTIME TESTS PASSED WITH 100% SUCCESS!")
            print("==========================================")
            
    except Exception as e:
        print("Test execution error:", e)
        raise e
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(run_cdp_tests())
