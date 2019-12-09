from glob import glob
import providers
from providers.util import call_batctl
import re

class Source(providers.DataSource):
    def required_args(self):
        return ['batadv_dev']

    def call(self, batadv_dev):
        lines = call_batctl(batadv_dev, ['o'])
        neighbours = {}
        prefix_lower = '/sys/class/net/{}/lower_'.format(batadv_dev)
        for dev in glob(prefix_lower + '*'):
            ifname = dev[len(prefix_lower):]
            mac = open(dev + '/address').read().strip()
            ifneighbours = {}
            for line in lines[2:]:
                for s in ['(', ')', '[', ']:', ']', '*']:
                    line = line.replace(s, '')
                fields = line.split()
                if fields[4] == ifname and fields[0] == fields[3]:
                    ifneighbours[fields[0]] = {'lastseen': float(fields[1].strip('s')), 'tq': int(fields[2])}
            neighbours[mac] = {'neighbours': ifneighbours}
        return neighbours
