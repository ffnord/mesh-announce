import providers

class Source(providers.DataSource):
    def required_args(self):
        return ['is_gateway']
    def call(self, is_gateway):
        return is_gateway
