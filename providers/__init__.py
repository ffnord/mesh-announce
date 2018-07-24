import os
import time
import traceback
from util import source_dirs, find_modules
from importlib import import_module

class DataSource():
    ''' Base data source, inherited by sources in provider directories
    '''
    def cache_ttl(self):
        ''' Default cache ttl, set to 0 to disable cache
        '''
        return 30

    def required_args(self):
        ''' Returns a list of required argument names
        '''
        return []

    def call(self, *args):
        ''' Override with actual implementation, args contains arguments listed
            in required_args in order
        '''
        raise NotImplementedError()



def _set_value(node, path, value):
    ''' Sets a value inside a complex data dictionary.
        The path Array must have at least one element.
    '''
    key = path[0]
    if len(path) == 1:
        node[key] = value
    elif key in node:
        _set_value(node[key], path[1:], value)
    else:
        node[path[0]] = {}
        _set_value(node[key], path[1:], value)

class SourceCache():
    ''' Simple singleton-based cache
    '''
    class CacheEntry():
        def __init__(self, key, value, ttl):
            self.key = key
            self.value = value
            self.expiry = time.monotonic() + ttl

        def isvalid(self):
            return time.time() < self.expiry

    instance = None

    @classmethod
    def getinstance(cls):
        if not cls.instance:
            cls.instance = cls()

        return cls.instance

    def __init__(self):
        self.cache = {}

    def put(self, key, value, ttl):
        self.cache[key] = self.CacheEntry(key, value, ttl)

    def has(self, key):
        return (key in self.cache) and self.cache[key].isvalid()

    def get(self, key):
        if not self.has(key):
            return None

        return self.cache[key].value

class InvalidSourceModuleExeption(Exception):
    def __init__(self, path):
        super().__init__(self, 'Invalid data source,' +
            ' module at "{}" does not spcify required member "Source"')

class Source():
    @classmethod
    def from_file(cls, modulepath, jsonpath):
        # construct a relative path
        relpath = '.'.join([''] + modulepath)
        # import modules relative to this package
        module = import_module(relpath, __package__)
        if not module.Source:
            raise InvalidSourceModuleExeption(relpath)

        return Source(jsonpath, module.Source())

    def __init__(self, path, source):
        self.path = path
        self.source = source

    def call(self, env):
        cache = SourceCache.getinstance()
        cache_result = cache.get(self)
        if cache_result:
            return cache_result

        args = []
        for argname in self.source.required_args():
            args.append(env[argname])

        result = self.source.call(*args)
        cache.put(self, result, self.source.cache_ttl())

        return result

class Provider():
    @classmethod
    def from_directory(cls, basepath, dirname):
        provider = Provider(dirname)

        sourcepaths = find_modules(os.path.join(basepath, dirname))
        for path in sourcepaths:
            for fname in path[1]:
                src = Source.from_file([dirname] + path[0] + [fname], path[0] + [fname])
                provider.add_source(src)

        return provider


    def __init__(self, name):
        self.name = name
        self.sources = []

    def add_source(self, source):
        self.sources.append(source)

    def call(self, env):
        ret = {}

        for source in self.sources:
            try:
                _set_value(ret, source.path, source.call(env))
            except:
                traceback.print_exc()

        return ret


def get_providers(directory):
    providers = {}

    if not os.path.isdir(directory):
        raise FileNotFoundError("The path '{}' is not a valid directory".format(directory))

    for dir in source_dirs(directory):
        provider = Provider.from_directory(directory, dir)

        providers[provider.name] = provider

    return providers
