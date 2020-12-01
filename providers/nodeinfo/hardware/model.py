import providers

class Source(providers.DataSource):
    def required_args(self):
        return ['hardware_model']
    def call(self, hardware_model):
        return hardware_model
