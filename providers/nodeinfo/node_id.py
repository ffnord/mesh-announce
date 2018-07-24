import providers
import socket

class Source(providers.DataSource):
    def required_args(self):
        return ['batadv_dev']

    def call(self, batadv_dev):
        return open('/sys/class/net/' + batadv_dev + '/address').read().strip().replace(':', '')
