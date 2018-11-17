#!/usr/bin/env python3

from http.server import HTTPServer, SimpleHTTPRequestHandler
from keyboard import Keyboard
from socketserver import ThreadingMixIn
from subprocess import call, STDOUT

KEYBOARD = Keyboard()
SERVER_PORT = 8080


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """
    Handle requests in a separate thread
    """
    daemon_threads = True


class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        """
        Serve a GET request
        """

        if ".png" in self.path:
            self.send_response(200)
            call(["/usr/bin/fbgrab", "-d", "/dev/fb0", "framebuffer.png"], stderr=STDOUT)
            self.send_header('Content-type', 'image/png')
            self.end_headers()

            with open("framebuffer.png", "rb") as fh:
                self.wfile.write(fh.read())

        else:
            with self.send_head() as fh:
                self.copyfile(fh, self.wfile)

    def do_POST(self):

        if self.path.endswith('key'):
            content_len = int(self.headers.get('content-length', 0))
            content = self.rfile.read(content_len).decode('ascii')
            jskc, state = content.split(',')
            KEYBOARD.send_key(int(jskc), int(state))

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write('{}'.encode('ascii'))


if __name__ == '__main__':
    print("Running on port {}".format(SERVER_PORT))
    httpd = ThreadedHTTPServer(('', SERVER_PORT), MyHandler)
    httpd.serve_forever()
