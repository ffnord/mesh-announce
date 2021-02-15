import providers
from providers.util import call


class Source(providers.DataSource):
    def call(self, vpn_proto):
        if 'fastd' == vpn_proto:
            return call(['fastd', '-v'])[0].split(' ')[1]

    def required_args(self):
        return ['vpn_proto']
