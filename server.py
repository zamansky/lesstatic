
from multiprocessing import Process
import SimpleHTTPServer, SocketServer,os
from config import config

def serve():
    os.chdir(config['site'])
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("",config['port']),Handler)
    print "Serving on port", config['port']
    print "Ctrl-C to exit"
    httpd.serve_forever()

def start_server():
    i = os.fork()
    if i==0:
        serve()
    else:
        return i


if __name__=="__main__":
    s = Server(6666)
    s.start()
