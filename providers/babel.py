import socket

BABEL_ADDR = ('::1', 33123)

def _reformat(entry):
    if entry[0] != 'add':
        return None
    d = {
            'add': entry[1]
    }
    for x in range(1, len(entry), 2):
        d[entry[x]] = entry[x+1]
    return d

def dump(addr=BABEL_ADDR):
	sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	sock.connect(addr)
	try:
		while True:
			data = str(sock.recv(1024), 'utf-8')
			if 'ok' in data:
				break

		sock.sendall(bytes('dump\n', 'utf-8'))

		input = ''
		while True:
			data = str(sock.recv(1024), 'utf-8')
			input += data
			if 'ok' in data:
				break
	finally:
		sock.close()
	return [ _reformat(x.split()) for x in input.split('\n') if x != 'ok' and x != '' ]

if __name__ == '__main__':
    print(dump())

