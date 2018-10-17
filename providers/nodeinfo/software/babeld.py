import providers
import socket

class Source(providers.DataSource):
    def required_args(self):
        return ['babel_addr']

    def call(self, babel_addr):
        if babel_addr is None:
            return None
        sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        sock.connect(babel_addr)
        input = ''
        try:
            while True:
                data = str(sock.recv(1024), 'utf-8')
                input += data
                if 'ok' in data:
                    break
        finally:
            sock.close()
        for d in input.split('\n'):
            x = d.split()
            if x[0] == 'version':
                return {
                    'version': x[1]
                }
        return None
