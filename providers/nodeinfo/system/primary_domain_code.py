import providers

class Source(providers.DataSource):
    def required_args(self):
        return ['primary_domain_code']

    def call(self, primary_domain_code):
        return primary_domain_code
