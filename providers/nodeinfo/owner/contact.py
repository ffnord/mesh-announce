import providers

class Source(providers.DataSource):
    def required_args(self):
        return ['contact']
    def call(self, contact):
        return contact
