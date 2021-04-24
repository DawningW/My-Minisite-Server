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

ROBOTS = """<pre>
User-agent: *
Disallow: /
</pre>"""

sites = {}

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
        global sites
        sites = self._args[0]
        logging.info("Server is running now.")
        self.serve_forever()
        return

    def stop(self):
        "停止HTTP服务器 TODO 未实现"
        # Thread._stop(self)
        return

class RequestHandler(BaseHTTPRequestHandler):
    "HTTP请求处理类"

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
            paths = path[1:].split("/")
            if paths[0] != "content" and paths[0] in sites:
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(sites[paths[0]].encode("utf-8"))
            elif paths[0] == "articles" and os.path.isfile("./static/articles/" + paths[1]):
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                f = open("./static/articles/" + paths[1], "r", encoding="utf-8")
                content = f.read()
                if paths[1].endswith(".md"):
                    content = md2html(content)
                content = wraphtml(content)
                self.wfile.write(content.encode("utf-8"))
                f.close()
            elif paths[0] == "static" and os.path.isfile("./static/" + paths[1]):
                # mimetype = imghdr.what("./data/" + paths[1]) # "image/{}".format(mimetype)
                mimetype = filetype.guess_mime("./static/" + paths[1])
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", mimetype)
                self.end_headers()
                f = open("./static/" + paths[1], "rb")
                shutil.copyfileobj(f, self.wfile)
                f.close()
            elif paths[0] == "robots.txt":
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(ROBOTS.encode("utf-8"))
            else:
                self.send_response(HTTPStatus.NOT_FOUND)
                self.end_headers()
        except ConnectionError as e:
            logging.error("Error: [%d] %s.", e.errno, e.strerror)
            pass
        return

    def do_POST(self):
        "HTTP POST"
        return

mdexts = ['markdown.extensions.extra', 'markdown.extensions.tables', 'markdown.extensions.toc']
def md2html(mdcontent):
    html = markdown.markdown(mdcontent, extensions = mdexts)
    return html

def wraphtml(content):
    return sites["content"].replace("{$content}", content)
