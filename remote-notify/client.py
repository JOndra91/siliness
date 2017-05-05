#!/usr/bin/python3

import argparse
from http import client
import json


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('--host', default='localhost')
    argp.add_argument('--port', default=6969, type=int)
    argp.add_argument(
        '--notify', default='/notify-send', const='/notify-send',
        dest='app', action='store_const')
    argp.add_argument(
        '--zenity', const='/zenity', dest='app', action='store_const')
    # argp.add_argument('--password')

    args, notify_args = argp.parse_known_args()

    body = json.dumps(notify_args)

    try:
        httpc = client.HTTPConnection(args.host, args.port)
        httpc.request('POST', args.app, body)

        response = httpc.getresponse()
        print(response.read())
    finally:
        httpc.close()

    # server_addr = (args.host, args.port)
    # httpd = server.HTTPServer(server_addr, NotifyHandler)
    # httpd.serve_forever()


if __name__ == '__main__':
    main()
