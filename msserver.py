# coding=utf-8

# 导入
import os
import logging
import json
import markdown
import imghdr
import filetype
from http.server import HTTPStatus, HTTPServer, BaseHTTPRequestHandler

sites = {}
server = None

def run(*args, **kwargs):
    address = args[0]
    port = args[1]
    logging.info("Starting server at a new thread, listening at: %s" % port)
    global sites, server
    sites = args[2]
    server = HTTPServer((address, port), RequestHandler)
    logging.info("Server is running now.")
    server.serve_forever()

class RequestHandler(BaseHTTPRequestHandler):
    "HTTP请求处理类"

    def do_HEAD(self):
        "HEAD request"
        self.send_response(HTTPStatus.OK)
        self.end_headers()
        return

    def do_GET(self):
        "HTTP GET"
        paths = self.path[1:].split("/")
        if paths[0] in sites:
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(sites[paths[0]].encode("utf-8"))
        elif paths[0] == "articles" and os.path.isfile("./data/" + paths[1]):
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            f = open("./data/" + paths[1], "r", encoding="utf-8")
            content = f.read()
            if paths[1].endswith(".md"):
                content = md2html(content)
            content = wraphtml(content)
            self.wfile.write(content.encode("utf-8"))
            f.close()
        elif paths[0] == "images" and os.path.isfile("./data/" + paths[1]):
            mimetype = imghdr.what("./data/" + paths[1])
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", 'image/{}'.format(mimetype))
            self.end_headers()
            f = open("./data/" + paths[1], "rb")
            self.wfile.write(f.read())
            f.close()
        elif paths[0] == "files" and os.path.isfile("./data/" + paths[1]):
            mimetype = filetype.guess_mime("./data/" + paths[1])
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", mimetype)
            self.end_headers()
            f = open("./data/" + paths[1], "rb")
            self.wfile.write(f.read())
            f.close()
        else:
            self.send_response(HTTPStatus.NOT_FOUND)
            self.end_headers()
        return

    def do_POST(self):
        "HTTP POST"

        return

mdexts = ['markdown.extensions.extra', 'markdown.extensions.tables', 'markdown.extensions.toc']
def md2html(mdcontent):
    html = markdown.markdown(mdcontent, extensions = mdexts)
    return html

def wraphtml(content):
    return sites["local"].replace("{$content}", content)
