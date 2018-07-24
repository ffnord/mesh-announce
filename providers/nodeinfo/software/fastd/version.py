import providers
from providers.util import call

class Source(providers.DataSource):
    def call(self):
        return call(['fastd','-v'])[0].split(' ')[1]
