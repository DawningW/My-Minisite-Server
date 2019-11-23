# coding=utf-8

# 导入
import os
import logging
import json
import markdown
import imghdr
import filetype
from http.server import HTTPStatus, HTTPServer, BaseHTTPRequestHandler

address = "127.0.0.1"
port = 80
server = None

sites = {}

def run(*args, **kwargs):
    logging.info("Starting server at a new thread, listening at: %s" % port)
    global server, sites
    sites = kwargs["sites"]
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
        if paths[0] == "minisite":
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(sites["kingsoft"].encode("utf-8"))
        elif paths[0] == "articles" and os.path.isfile("./data/" + paths[1]):
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            f = open("./data/" + paths[1], "rb")
            content = f.read()
            if paths[1].endswith(".md"):
                content = md2html(content)
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

mdexts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables', 'markdown.extensions.toc']
def md2html(mdcontent):
    html = markdown.markdown(mdcontent, extensions = mdexts)
    content = Markup(html)
    return content
