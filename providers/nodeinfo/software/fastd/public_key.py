import providers


class Source(providers.DataSource):
    def call(self, vpn_pubkey):
        return vpn_pubkey

    def required_args(self):
        return ['vpn_pubkey']
