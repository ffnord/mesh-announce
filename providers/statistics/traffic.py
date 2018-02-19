import providers
from providers.util import call

class Source(providers.DataSource):
    def required_args(self):
        return ['batadv_dev']

    def call(self, batadv_dev):
        return (lambda fields:
            dict(
                (key, dict(
                    (type_, int(value_))
                    for key_, type_, value_ in fields
                        if key_ == key))
                for key in ['rx', 'tx', 'forward', 'mgmt_rx', 'mgmt_tx']
            )
        )(list(
            (
                key.replace('_bytes', '').replace('_dropped', ''),
                'bytes' if key.endswith('_bytes') else 'dropped' if key.endswith('_dropped') else 'packets',
                value
            )
            for key, value in map(lambda s: list(map(str.strip, s.split(': ', 1))), call(['ethtool', '-S', batadv_dev])[1:])
        ))
