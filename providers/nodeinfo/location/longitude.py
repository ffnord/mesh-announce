import providers

class Source(providers.DataSource):
    def required_args(self):
        return ['longitude']
    def call(self, longitude):
        return longitude
