import providers
from util import check_process_running



class Source(providers.DataSource):
    def call(self, vpn_proto):
        if 'fastd' == vpn_proto:
            try:
                return check_process_running('fastd')
            except ImportError:
                return True

    def required_args(self):
        return ['vpn_proto']
