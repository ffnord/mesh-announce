import providers

class Source(providers.DataSource):
    def required_args(self):
        return ['mesh_ipv4']

    def call(self, mesh_ipv4):
        return { "ipv4": mesh_ipv4 }
