
from multiprocessing import Process
import SimpleHTTPServer, SocketServer,os

from config import config

class Server(Process):
    def __init__(self,p):
        self.port = int(p)
        super(Server,self).__init__()

    def run(self):
        os.chdir(config['site'])
        Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer(("",self.port),Handler)
        print "Serving on port", self.port
        print "Ctrl-C to exit"
        httpd.serve_forever()

if __name__=="__main__":
    s = Server(6666)
    s.start()
