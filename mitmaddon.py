import mitmproxy
from mitmproxy import ctx
from mitmproxy import http

class myproxy:
    "mitmproxy的插件,用于将对热点新闻的访问重定向到我的服务器上"
    def request(self, flow: http.HTTPFlow) -> None:
        "发出请求"
        key = getKey(flow.request.headers.keys(), "user-agent")
        if key != "" and "MyMinisiteServer" not in flow.request.headers[key]:
            if flow.request.host == "hotnews.duba.com" and flow.request.path.startswith("/"):
                fullpath = flow.request.path
                if fullpath.startswith("/"): fullpath = fullpath[1:]
                if fullpath.endswith("/"): fullpath = fullpath[:-1]
                paths = fullpath.split("/")
                print(paths)
                if paths[0] == "minisite" and len(paths) >= 2 and (paths[1] == "default" or paths[1].isdigit()):
                    if len(paths) >= 3 and (".htm" not in paths[2] and "?" not in paths[2]):
                        return
                    ctx.log.info("发现用户毒霸热点访问,进行重定向")
                    flow.request.host = "127.0.0.1"
                    flow.request.port = 81
                    flow.request.path = "/kingsoft/default"

def getKey(list, key) -> str:
    for value in list:
        if value.lower() == key.lower():
            return value
    return ""

addons = [
    myproxy()
]
