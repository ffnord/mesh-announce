import providers

class Source(providers.DataSource):
    def required_args(self):
        return ['latitude']
    def call(self, latitude):
        return latitude
