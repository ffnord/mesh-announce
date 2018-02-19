import providers

class Source(providers.DataSource):
    def call(self):
        return open('/sys/module/batman_adv/version').read().strip()
