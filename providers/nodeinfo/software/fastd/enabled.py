import providers
from util import check_process_running


class Source(providers.DataSource):
    def call(self):
        try:
            return check_process_running('fastd')
        except ImportError:
            return True
