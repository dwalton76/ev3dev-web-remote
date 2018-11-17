#!/usr/bin/env python

import BaseHTTPServer
import SimpleHTTPServer
import SocketServer
import subprocess
from keyboard import Keyboard

KEYBOARD = Keyboard()
SERVER_PORT = 8080


class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """
    Handle requests in a separate thread
    """
    daemon_threads = True


class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        """
        Serve a GET request
        """

        if ".png" in self.path:
            self.send_response(200)
            self.send_header('Content-Type', 'multipart/x-mixed-replace;boundary=boundarydonotcross')
            self.end_headers()

            subprocess.call(["/usr/bin/fbgrab", "-d", "/dev/fb0", "framebuffer.png"], stderr=subprocess.STDOUT)
            self.send_header('Content-type', 'image/png')
            self.end_headers()

            with open("framebuffer.png", "rb") as fh:
                self.wfile.write(fh.read())

        else:
            f = self.send_head()
            if f:
                try:
                    self.copyfile(f, self.wfile)
                finally:
                    f.close()

    def do_POST(self):

        if self.path.endswith('key'):
            self.send_response(200)
            content_len = int(self.headers.getheader('content-length', 0))
            content = self.rfile.read(content_len)
            jskc, state = content.split(',')
            KEYBOARD.send_key(int(jskc), int(state))


if __name__ == '__main__':
    print("Running on port {}".format(SERVER_PORT))
    httpd = ThreadedHTTPServer(('', SERVER_PORT), MyHandler)
    httpd.serve_forever()
