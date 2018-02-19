import providers
from glob import glob

class Source(providers.DataSource):
    def required_args(self):
        return ['batadv_dev']

    def call(self, batadv_dev):
        return (lambda neighbours: {
            open("{}/address".format(path)).read().strip(): {"neighbours": {
                neigh[0]: {"lastseen": neigh[1], "tq": neigh[2]}
                for neigh in neighbours
                if neigh[3] == path[len('/sys/class/net/{}/lower_'.format(batadv_dev)):]
            }}
            for path in
                glob('/sys/class/net/{}/lower_*'.format(batadv_dev))
        })([
            (line[0], float(line[1].strip('s')), int(line[2].strip(')')), line[4].strip('[]:'))
            for line in map(lambda l: l.replace('(', '').replace('[', '').split(),
                open('/sys/kernel/debug/batman_adv/{}/originators'.format(batadv_dev)))
            if line[0] == line[3]
        ])
