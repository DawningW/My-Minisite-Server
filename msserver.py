# coding=utf-8

# 导入
import os
import logging
import json
import markdown
# import imghdr
import filetype
import shutil
from threading import Thread
from socketserver import ThreadingMixIn, TCPServer
from http.server import HTTPStatus, HTTPServer, BaseHTTPRequestHandler

ROBOTS_TXT = """<pre>
User-agent: *
Disallow: /
</pre>"""

sites = {}
enable_robotstxt = False

test_ip = []

class ThreadingHTTPServer(Thread, ThreadingMixIn, HTTPServer):
    def __init__(self, address, port, *args, **kwargs):
        Thread.__init__(self, daemon = True, args = args, kwargs = kwargs)
        HTTPServer.__init__(self, (address, port), RequestHandler)
        return

    def start(self):
        "启动HTTP服务器"
        logging.info("Starting server at a new thread, listening at: %s" % self.server_port)
        Thread.start(self)
        return

    def run(self):
        global sites, enable_robotstxt
        sites, enable_robotstxt = self._args
        logging.info("Server is running now.")
        self.serve_forever()
        return

    def stop(self):
        "停止HTTP服务器 TODO 未实现"
        # Thread._stop(self)
        return

class RequestHandler(BaseHTTPRequestHandler):
    "HTTP请求处理类"

    def log_message(self, format, *args):
        print("\r[%s] %s %s" %
                         (self.log_date_time_string(),
                          self.address_string(),
                          format % args))
        print(">> ", end = '', flush = True)
        return

    def address_string(self):
        real_ip = self.headers.get("X-Forwarded-For", self.client_address[0])
        if test_ip.count(real_ip) == 0:
            ua = self.headers.get("User-Agent", "No User Agent")
            logging.info("%s User-Agent: %s" % (real_ip, ua))
            test_ip.append(real_ip)
        return real_ip

    def handle_one_request(self):
        if not self.wfile.closed:
            super().handle_one_request()
        else:
            self.close_connection = True
        return

    def do_HEAD(self):
        "HEAD request"
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        return

    def do_GET(self):
        "HTTP GET"
        try:
            path, sep, arg = self.path.partition("?")
            if arg != "":
                logging.info("%s GET %s" % (self.address_string(), self.path))
                pass
            paths = path[1:].split("/")
            if paths[0] != "content" and paths[0] in sites:
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(sites[paths[0]].encode("utf-8"))
            elif paths[0] == "articles" and os.path.isfile("./assets/articles/" + paths[1]):
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                f = open("./assets/articles/" + paths[1], "r", encoding="utf-8")
                content = f.read()
                if paths[1].endswith(".md"):
                    content = md2html(content)
                content = wraphtml(content)
                self.wfile.write(content.encode("utf-8"))
                f.close()
            elif paths[0] == "static" and os.path.isfile("./assets/" + '/'.join(paths[1:])):
                # mimetype = imghdr.what("./assets/" + '/'.join(paths[1:])) # "image/{}".format(mimetype)
                mimetype = filetype.guess_mime("./assets/" + '/'.join(paths[1:]))
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", mimetype)
                self.send_header("Cache-Control", "max-age=3600")
                self.end_headers()
                f = open("./assets/" + '/'.join(paths[1:]), "rb")
                shutil.copyfileobj(f, self.wfile)
                f.close()
            elif paths[0] == "robots.txt" and enable_robotstxt:
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(ROBOTS_TXT.encode("utf-8"))
            else:
                self.send_response(HTTPStatus.NOT_FOUND)
                self.end_headers()
        except ConnectionError as e:
            self.log_error("Error: [%d] %s", e.errno, e.strerror)
            pass
        return

    def do_POST(self):
        "HTTP POST"
        self.send_response(HTTPStatus.NOT_FOUND)
        self.end_headers()
        return

mdexts = ['markdown.extensions.extra', 'markdown.extensions.tables', 'markdown.extensions.toc']
def md2html(mdcontent):
    html = markdown.markdown(mdcontent, extensions = mdexts)
    return html

def wraphtml(content):
    return sites["content"].replace("{$content}", content)
