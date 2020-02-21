import providers

class Source(providers.DataSource):
    def required_args(self):
        return ['domain_code']

    def call(self, domain_code):
        return domain_code
