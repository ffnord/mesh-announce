import providers
from providers.util import call

class Source(providers.DataSource):
    def required_args(self):
        return ['batadv_dev']

    def call(self, batadv_dev):
        return {
            batadv_dev: {
                "interfaces": {
                    "tunnel": [
                        open('/sys/class/net/{}/address'.format(iface)).read().strip()
                        for iface in map(
                            lambda line: line.split(':')[0],
                            call(['batctl', '-m', batadv_dev, 'if'])
                        )
                    ]
                }
            }
        }
