import socket
import threading

class Receiver:
    def __init__(self, options, summary):
        self.options = options
        self.summary = summary
        self.runable = True
        self.socket = socket.socket(socket.AF_INET, options.protocol)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((None, options.port))

    def listen(self):
        self.socket.listen(3)
        while self.runable:
            client, address = self.socket.accept()
            client.settimeout(60)
            threading.Thread(
                target = self.receive, args = (client,address)
            ).start()
        self.socket.close()

    def receive(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    client.send("ACK")
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False


class Sender:
    def __init__(self, options, summary):
        self.options = options
        self.summary = summary
        self.runable = True



# some example code ofund on the web -------------------------------------------
class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(
                target = self.listenToClient, args = (client,address)
            ).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    response = data
                    client.send(response)
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    while True:
        port_num = input("Port? ")
        try:
            port_num = int(port_num)
            break
        except ValueError:
            pass

    ThreadedServer('',port_num).listen()
