#!/usr/bin/python3

import argparse
from http import server
import json
import subprocess


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('--host', default='0.0.0.0')
    argp.add_argument('--port', default=6969, type=int)
    # argp.add_argument('--password')

    args = argp.parse_args()

    server_addr = (args.host, args.port)
    httpd = server.HTTPServer(server_addr, NotifyHandler)
    httpd.serve_forever()


class NotifyHandler(server.BaseHTTPRequestHandler):

    def do_POST(self):

        binary = self.path[1:]
        if binary not in ['notify-send', 'zenity']:
            self.send_response_only(403)
            self.end_headers()
            return

        try:
            length = int(self.headers.get('Content-Length', 0))
            content = self.rfile.read(length).decode('utf-8')
            request = json.loads(content)
            if type(request) is list:
                app = subprocess.run(
                    [binary] + request, stderr=subprocess.PIPE)
                if app.returncode == 0:
                    self.send_response_only(200)
                else:
                    self.send_response(500)
                self.end_headers()
                self.wfile.write(app.stderr)
            else:
                self.send_response_only(400)
                self.end_headers()
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(str(e))


if __name__ == '__main__':
    main()
