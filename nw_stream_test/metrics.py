import threading
import time

class Message:
    def __init__(self, host, raw):
        self.created = time.time()
        self.host = host
        self.raw = raw
        if raw is None:
            self.size = 0
        else:
            self.size = len(raw)

class MessageList:
    def __init__(self):
        self.bytes = 0
        self.errors = 0
        self.messages = []

class Totals:
    def __init__(self):
        self.received = MessageList()
        self.sent = MessageList()

class Summary:
    def __init__(self, cleaner_wait=1, timeout=60):
        self.received = MessageList()
        self.sent = MessageList()
        self.timeout = timeout
        self.runable = True
        self.thread = threading.Thread(name="cleaner", target=self.cleaner)
        self.thread.start()
        self.totals = Totals()

    def receive(self, message):
        self.received.messages.append(message)

    def send(self, message):
        self.sent.messages.append(message)

    def cleaner(self, wait=1):
        while self.runable:
            time.sleep(wait)
            old = time.time() - self.timeout
            if len(self.received.messages) > 0:
                message = self.received.messages[0]
                while message.created < old and len(self.received.messages):
                    self.received.messages.pop(0)
                    message = self.received.messages[0]
            if len(self.sent.messages) > 0:
                message = self.sent.messages[0]
                while message.created < old and len(self.sent.messages):
                    self.sent.messages.pop(0)
                    message = self.sent.messages[0]
            errors = 0
            bytes = 0
            for message in self.received.messages:
                if message.size < 1:
                    errors += 1
                bytes += message.size
            self.received.errors = errors
            self.received.bytes = bytes
            errors = 0
            bytes = 0
            for message in self.sent.messages:
                if message.size < 1:
                    errors += 1
                bytes += message.size
            self.sent.errors = errors
            self.sent.bytes = bytes

    def stop(self):
        self.runable = False
