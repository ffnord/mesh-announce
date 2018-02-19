import providers

class Source(providers.DataSource):
    def call(self):
        return dict(zip(('running', 'total'), map(int, open('/proc/loadavg').read().split(' ')[3].split('/'))))
