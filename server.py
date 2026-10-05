import http.server
import json
import os
import socketserver
import sys

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)
import traceback
import build_map

JSON_PATH = os.path.join(WORKSPACE_DIR, 'locs_gps.json')
HTML_PATH = os.path.join(WORKSPACE_DIR, 'kaart_bedieningen.html')
ARTIFACT_DIR = r'C:\Users\bartvercaempst\.gemini\antigravity\brain\ef3e86e7-5525-45fe-83e0-530122591b51'
ARTIFACT_HTML = os.path.join(ARTIFACT_DIR, 'kaart_bedieningen.html')

PORT = 8055

class GPSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WORKSPACE_DIR, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok', 'port': PORT}).encode('utf-8'))
            return
        elif self.path == '/' or self.path == '/kaart':
            self.send_response(302)
            self.send_header('Location', '/kaart_bedieningen.html')
            self.end_headers()
            return
        else:
            # Serve files with CORS
            super().do_GET()

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_POST(self):
        if self.path == '/api/save':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                payload = json.loads(post_data.decode('utf-8'))
                loc_id = payload.get('id')
                lat = float(payload.get('lat'))
                lng = float(payload.get('lng'))

                # Update locs_gps.json
                with open(JSON_PATH, 'r', encoding='utf-8') as f:
                    db = json.load(f)

                updated = False
                for loc in db.get('locations', []):
                    if loc['id'] == loc_id:
                        loc['lat'] = lat
                        loc['lng'] = lng
                        updated = True
                        break

                if not updated:
                    for idx, b in enumerate(db.get('bundels', [])):
                        if f'bundel_{idx}' == loc_id:
                            b['lat'] = lat
                            b['lng'] = lng
                            updated = True
                            break

                if updated:
                    with open(JSON_PATH, 'w', encoding='utf-8') as f:
                        json.dump(db, f, indent=2, ensure_ascii=False)

                    # Re-generate HTML
                    import build_map
                    html_content = build_map.build_map_html(db['locations'], db.get('bundels', []))
                    with open(HTML_PATH, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    if os.path.exists(ARTIFACT_DIR):
                        with open(ARTIFACT_HTML, 'w', encoding='utf-8') as f:
                            f.write(html_content)

                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True, 'id': loc_id, 'lat': lat, 'lng': lng}).encode('utf-8'))
                    print(f"[GPS Update] {loc_id} opgeslagen op Lat: {lat}, Lng: {lng}")
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Locatie niet gevonden'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def main():
    with socketserver.TCPServer(('', PORT), GPSRequestHandler) as httpd:
        print(f"DB Cargo GPS Kaart Server gestart op http://localhost:{PORT}")
        print("Wijzigingen in coördinaten worden automatisch direct opgeslagen naar:")
        print(f" -> {JSON_PATH}")
        print(f" -> {HTML_PATH}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer gestopt.")

if __name__ == '__main__':
    main()
