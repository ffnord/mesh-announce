import providers
from providers.util import call

class Source(providers.DataSource):
    def call(self):
        try:
            return {
                "enabled": True,
                "version": call(['fastd','-v'])[0].split(' ')[1],
            }
        except:
            return None
