import socket

from configparser import ConfigParser

class GlobalOptions():
    ''' Container class for global options
    '''
    def __init__(self, port, default_domain):
        self.port = port
        self.default_domain = default_domain

class DomainOptions():
    ''' Base container class for per domain options
    '''
    @classmethod
    def from_parser(cls, section, parser, globals):
        ''' Builds a DomainOptions object from a config section
            Handles domain type specific options automatically
        '''
        from domain import DomainType

        domain_type = parser.get(section, 'DomainType', fallback='simple')
        # Get DomainOptions subclass for type and instantiate
        return DomainType.get(domain_type.lower()).options(section, parser, globals)

    def __init__(self, name, parser, globals):
        ''' Initialize common options
        '''
        from domain import Domain

        self.contact = parser.get(name, 'Contact', fallback=None)
        self.hardware_model = parser.get(name, 'Hardware-Model', fallback=None)
        self.hostname = parser.get(name, 'Hostname', fallback=socket.gethostname())
        self.name = name
        self.interfaces = list(map(str.strip, parser.get(name, 'Interfaces', fallback='').split(',')))
        self.is_gateway = parser.getboolean(name, 'VPN', fallback='True')
        self.longitude = parser.getfloat(name, 'Longitude', fallback=None)
        self.latitude = parser.getfloat(name, 'Latitude', fallback=None)
        self.mcast_link = parser.get(name, 'MulticastLinkAddress', fallback='ff02::2:1001')
        self.mcast_site = parser.get(name, 'MulticastSiteAddress', fallback='ff05::2:1001')
        self.ipv4_gateway = parser.get(name, 'IPv4Gateway', fallback=None)
        self.domain_type = Domain

class BatmanDomainOptions(DomainOptions):
    ''' Container for batman specific options
    '''
    def __init__(self, name, parser, globals):
        ''' Initialize common and batman-specific options
        '''
        from domain import BatadvDomain

        # Parse common options
        super().__init__(name, parser, globals)
        # Parse batman specific options
        self.batman_iface = parser.get(name, 'BatmanInterface', fallback='bat-' + name)
        self.domain_type = BatadvDomain

class Config():
    ''' Represents a parsed config file
    '''
    @classmethod
    def from_file(cls, fname):
        ''' Load config from file
        '''
        parser = ConfigParser(empty_lines_in_values=False, default_section='Defaults')
        with open(fname) as file:
            parser.read_file(file)
        return cls(parser)

    def __init__(self, parser):
        ''' load config from a config parser
        '''
        self._initialize_global_options(parser)
        self.domains = { }
        for domain in parser.sections():
            self._initialize_domain_options(parser, domain)
            if not self.globals.default_domain:
                self.globals.default_domain = self.domains[domain]

    def _initialize_global_options(self, parser):
        ''' Set all global options
        '''
        self.globals = GlobalOptions(
            parser.getint('Defaults', 'Port', fallback=1001),
            parser.get('Defaults', 'DefaultDomain', fallback=None)
        )

    def _initialize_domain_options(self, parser, domain):
        ''' Populate options for domain from config parser
        '''
        self.domains[domain] = DomainOptions.from_parser(domain, parser, self.globals)

    def get_domain_names(self):
        ''' Get list of all domain names listed in the config
        '''
        return self.domains.keys()

    def get_port(self):
        return self.globals.port

    def get_default_domain(self):
        return self.globals.default_domain

    def get_domain_config(self, domain):
        return self.domains[domain]
