import providers

class Source(providers.DataSource):
    def required_args(self):
        return ['batadv_dev']

    def call(self, batadv_dev):
        if batadv_dev is None:
            node_id = open('/etc/machine-id').read().strip()
            return "{0}:{1}:{2}:{3}:{4}:{5}".format(node_id[0:2],node_id[2:4],node_id[4:6],node_id[6:8],node_id[8:10],node_id[10:12])
        return open('/sys/class/net/' + batadv_dev + '/address').read().strip()
