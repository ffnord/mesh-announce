import providers

class Source(providers.DataSource):
    def call(self):
        return dict(
            (key.replace('Mem', '').lower(), int(value.split(' ')[0]))
            for key, value in map(lambda s: map(str.strip, s.split(': ', 1)), open('/proc/meminfo').readlines())
            if key in ('MemTotal', 'MemFree', 'Buffers', 'Cached')
        )
