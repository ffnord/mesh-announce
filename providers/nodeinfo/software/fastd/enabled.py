import providers
from util import check_process_running


class Source(providers.DataSource):
    def call(self):
        return check_process_running('fastd')
