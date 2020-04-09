import providers

class Source(providers.DataSource):
    def required_args(self):
        return ['batadv_dev', 'domain_code', 'known_codes']

    def call(self, batadv_dev, domain_code, known_codes):
        try:
            return known_codes[batadv_dev]
        except KeyError:
            return domain_code
