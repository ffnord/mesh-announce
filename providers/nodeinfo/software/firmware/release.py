import providers
from providers.util import call

class Source(providers.DataSource):
    def call(self):
        return call(['lsb_release','-rs'])[0]
