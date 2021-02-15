import providers


class Source(providers.DataSource):
    def call(self, vpn_proto, vpn_pubkey):
        if 'fastd' == vpn_proto:
            return vpn_pubkey

    def required_args(self):
        return ['vpn_proto', 'vpn_pubkey']
