#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   ScoreCache.py    
@Contact :   huanghoward@foxmail.com
@Modify Time :    2022/4/18 15:55  
------------      
"""
import collections

import numpy as np


class Cache:
    """
    LRU cache. if the capacity is None, it is a infinite Cache.
    """

    def __init__(self, LocalScoreFunc, capacity=None):
        print("initial")
        self.LocalScoreFunc = LocalScoreFunc
        # for one data, there is one cache.
        self.caches = {}
        self.capacity = capacity

    def __call__(self, *args, **kwargs):
        data_hash = None
        i = None
        Pai = ()
        for arg in args:
            if isinstance(arg, np.ndarray):
                data = arg
                data_hash = data.shape
            elif isinstance(arg, int):
                i = arg
            elif isinstance(arg, list):
                Pai = tuple(arg)

        value = self.get(data_hash, i, Pai)
        if value is None:
            value = self.LocalScoreFunc(*args, **kwargs)
        self.set(data_hash, i, Pai, value)
        return value

    def get(self, data_hash, i, Pai):
        if data_hash in self.caches.keys():
            cache = self.caches[data_hash]
        else:
            self.caches[data_hash] = collections.OrderedDict()
            cache = self.caches[data_hash]
        if (i, Pai) in cache.keys():
            value = cache.pop((i, Pai))
            cache[(i, Pai)] = value
            return value
        else:
            return None

    def set(self, data_hash, i, Pai, value):
        if data_hash in self.caches.keys():
            cache = self.caches[data_hash]
        else:
            self.caches[data_hash] = collections.OrderedDict()
            cache = self.caches[data_hash]

        if self.capacity is not None:
            if (i, Pai) in cache.keys():
                cache.pop((i, Pai))
                cache[(i, Pai)] = value
            else:
                if len(cache) >= self.capacity:
                    cache.popitem(last=False)
                    cache[(i, Pai)] = value
                else:
                    cache[(i, Pai)] = value
        else:
            if (i, Pai) not in cache.keys():
                cache[(i, Pai)] = value
