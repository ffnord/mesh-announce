import providers
import socket

class Source(providers.DataSource):
    def call(self):
        return socket.gethostname()
