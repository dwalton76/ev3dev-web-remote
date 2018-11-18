#!/usr/bin/env python3

import logging
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from keyboard import Keyboard
from socketserver import ThreadingMixIn
from subprocess import call, STDOUT
from time import sleep

KEYBOARD = Keyboard()
SERVER_PORT = 8080
pre_key_down_mtime = None
key_string = {
    8 : 'BACK',
    38 : 'UP',
    37 : 'LEFT',
    13 : 'ENTER',
    39 : 'RIGHT',
    40 : 'DOWN',
}
DEVNULL = open(os.devnull, 'w')


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

        if "framebuffer.png" in self.path:
            self.send_response(200)
            call(["/usr/bin/fbgrab", "-d", "/dev/fb0", "framebuffer.png"],
                stdout=DEVNULL, stderr=STDOUT)
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
            jskc = int(jskc)
            state = int(state)

            # key down: note the timestamp of when the framebuffer was last modified
            if state:
                log.info("key down: {}".format(key_string.get(jskc, jskc)))
                global pre_key_down_mtime
                pre_key_down_mtime = os.path.getmtime("/dev/fb0")
            else:
                log.info("key up  : {}".format(key_string.get(jskc, jskc)))

            KEYBOARD.send_key(jskc, state)

            # key up: when the user presses down on a key that will cause the
            # framebuffer to update but if they release the key very quickly it
            # could be so fast that the framebuffer has not been updated yet.
            #
            # On a key up, block until the framebuffer has been modified from
            # the key down.
            if not state:
                while os.path.getmtime("/dev/fb0") == pre_key_down_mtime:
                    sleep(0.01)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write('{}'.encode('ascii'))

    def log_message(self, format, *args):
        """
        log using our own handler instead of BaseHTTPServer's
        """
        # log.debug(format % args)
        pass


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)5s: %(message)s")
    log = logging.getLogger(__name__)

    print("Running on port {}".format(SERVER_PORT))
    httpd = ThreadedHTTPServer(('', SERVER_PORT), MyHandler)
    httpd.serve_forever()
