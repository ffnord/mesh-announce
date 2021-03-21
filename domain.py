from config import BatmanDomainOptions, DomainOptions

class Domain():
    ''' Abstract container object for a freifunk domain
    '''
    def __init__(self, config):
        self.config = config

    def get_contact(self):
        return self.config.contact

    def get_domain_code(self):
        return self.config.domain_code

    def get_name(self):
        return self.config.name

    def get_ipv4_gateway(self):
        return self.config.ipv4_gateway

    def get_hardware_model(self):
        return self.config.hardware_model

    def get_hostname(self):
        return self.config.hostname

    def get_multicast_address_link(self):
        return self.config.mcast_link

    def get_multicast_address_site(self):
        return self.config.mcast_site

    def get_latitude(self):
        return self.config.latitude

    def get_longitude(self):
        return self.config.longitude

    def is_gateway(self):
        return self.config.is_gateway

    def get_fastd_pubkey(self):
        return self.config.fastd_pubkey

    def get_wireguard_pubkey(self):
        return self.config.wireguard_pubkey

    def get_vpn_protos(self):
        return self.config.vpn_protos

    def get_interfaces(self):
        ''' Returns list off all interfaces respondd queries are
            expected to arrive on
        '''
        return self.config.interfaces

    def get_provider_args(self):
        ''' Returns dict of parameters respondd queries are
            expected to arrive on
        '''
        return {
            'contact': self.get_contact(),
            'domain_code': self.get_domain_code(),
            'primary_domain_code': self.get_name(),
            'hardware_model': self.get_hardware_model(),
            'hostname': self.get_hostname(),
            'is_gateway': self.is_gateway(),
            'latitude': self.get_latitude(),
            'longitude': self.get_longitude(),
            'mesh_ipv4': self.get_ipv4_gateway(),
            'fastd_pubkey': self.get_fastd_pubkey(),
            'wireguard_pubkey': self.get_wireguard_pubkey(),
            'vpn_protos': self.get_vpn_protos()
        }

class BatadvDomain(Domain):
    ''' Container object for a batman freifunk domain
    '''
    def __init__(self, config):
        super().__init__(config)

    def get_interfaces(self):
        return super().get_interfaces() + [self.get_batman_interface()]

    def get_batman_interface(self):
        return self.config.batman_iface

    def get_provider_args(self):
        args = super().get_provider_args()
        args.update({ 'batadv_dev': self.get_batman_interface() })
        return args

class DomainRegistry():
    ''' Simple singleton based registry for freifunk domains
    '''
    instance = None
    @classmethod
    def get_instance(cls):
        if not cls.instance:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        self.domain_by_iface = { }
        self.default_domain = None

    def add_domain(self, dom):
        for iface in dom.get_interfaces():
            self.domain_by_iface[iface] = dom

    def get_domain_by_interface(self, iface):
        if iface in self.domain_by_iface:
            return self.domain_by_iface[iface]
        return None

    def get_interfaces(self):
        ''' Get all domain interfaces known to this registry
        '''
        return self.domain_by_iface.keys()

    def get_default_domain(self):
        return self.default_domain

    def set_default_domain(self, dom):
        self.default_domain = dom

class DomainType():
    ''' Domain type, links domain type to its options
    '''
    @staticmethod
    def get(name):
        if not name in domain_types:
            raise Exception("Unknown domain type")
        return domain_types[name]

    def __init__(self, name, options, domain_type):
        self.name = name
        self.options = options
        self.domain_type = domain_type

# List of domain types, key is used as domain type in config
# Use only lower case keys, domain type from config is converted to lower
# case during parsing
domain_types = {
    'simple': DomainType('simple', DomainOptions, Domain),
    'batadv': DomainType('batadv', BatmanDomainOptions, BatadvDomain),
}

