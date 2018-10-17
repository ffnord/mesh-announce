import providers
import socket

class Source(providers.DataSource):
    def required_args(self):
        return ['batadv_dev']

    def call(self, batadv_dev):
        if batadv_dev is None:
            return open('/etc/machine-id').read().strip()[:12]
        return open('/sys/class/net/' + batadv_dev + '/address').read().strip().replace(':', '')
