from socketserver import BaseRequestHandler, TCPServer
from time import sleep
from threading import Thread
from logic import inst_logic


class Handler(BaseRequestHandler):
    def handle(self):
        while True:
            msg = self.request.recv(1024)
            if msg:
                try:
                    msg = msg.decode("utf-8")
                except UnicodeDecodeError as e:
                    print(e)
                else:
                    inst_logic.msg_decision(msg)
            else:
                break
            sleep(0.1)


Server_inst = TCPServer(('', 10000), Handler)
Server_thread = Thread(target=Server_inst.serve_forever)
Server_thread.daemon = True
