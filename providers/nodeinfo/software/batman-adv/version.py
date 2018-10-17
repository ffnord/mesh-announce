import providers

class Source(providers.DataSource):
    def required_args(self):
        return ['batadv_dev']

    def call(self, batadv_dev):
        if batadv_dev is None:
            return None
        return open('/sys/module/batman_adv/version').read().strip()
