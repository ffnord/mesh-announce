import providers
from providers.util import call


class Source(providers.DataSource):
    def call(self, vpn_protos):
        if 'fastd' in vpn_protos:
            return call(['fastd', '-v'])[0].split(' ')[1]

    def required_args(self):
        return ['vpn_protos:fastd']
