from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

BASE_PATH = r"C:\Users\kanam\.n8n-files\outputs\accounts"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Allow cross origin requests from dashboard
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        if self.path == '/accounts':
            accounts = []
            for account_id in os.listdir(BASE_PATH):
                account_path = os.path.join(BASE_PATH, account_id)
                if os.path.isdir(account_path):
                    account = {"account_id": account_id}

                    # Read v1 memo
                    v1_path = os.path.join(account_path, 'v1', 'account_memo.json')
                    if os.path.exists(v1_path):
                        with open(v1_path, 'r') as f:
                            account['v1'] = json.load(f)

                    # Read v2 memo
                    v2_path = os.path.join(account_path, 'v2', 'account_memo.json')
                    if os.path.exists(v2_path):
                        account['v2'] = json.load(open(v2_path))

                    # Read changelog
                    cl_path = os.path.join(account_path, 'changelog', 'changelog.json')
                    if os.path.exists(cl_path):
                        account['changelog'] = json.load(open(cl_path))

                    accounts.append(account)

            self.wfile.write(json.dumps(accounts).encode())

        elif self.path.startswith('/account/'):
            account_id = self.path.split('/')[-1]
            account_path = os.path.join(BASE_PATH, account_id)
            data = {"account_id": account_id}

            v1_path = os.path.join(account_path, 'v1', 'account_memo.json')
            if os.path.exists(v1_path):
                with open(v1_path) as f:
                    data['v1'] = json.load(f)

            v2_path = os.path.join(account_path, 'v2', 'account_memo.json')
            if os.path.exists(v2_path):
                with open(v2_path) as f:
                    data['v2'] = json.load(f)

            cl_path = os.path.join(account_path, 'changelog', 'changelog.json')
            if os.path.exists(cl_path):
                with open(cl_path) as f:
                    data['changelog'] = json.load(f)

            self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        print(f"[Clara Server] {args[0]} {args[1]}")

print("✅ Clara Dashboard Server running at http://localhost:8000")
HTTPServer(('localhost', 8000), Handler).serve_forever()
