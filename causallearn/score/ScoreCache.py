#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   ScoreCache.py    
@Contact :   huanghoward@foxmail.com
@Modify Time :    2022/4/18 15:55  
------------      
"""

import numpy as np


class Cache:
    """
    simple caching without ordering or size limit.
    """
    def __init__(self, LocalScoreFunc):
        self.LocalScoreFunc = LocalScoreFunc
        self.caches = {}

    def __call__(self, *args, **kwargs):
        data_hash = None
        i = None
        Pai = ()
        for arg in args:
            if isinstance(arg, np.ndarray):
                data = arg
                data_hash = data.tobytes()
            elif isinstance(arg, int):
                i = arg
            elif isinstance(arg, list):
                Pai = tuple(arg)
        if data_hash not in self.caches.keys():
            self.caches[data_hash] = {}

        cache = self.caches[data_hash]
        if (i, Pai) in cache.keys():
            return cache[(i, Pai)]
        else:
            score = self.LocalScoreFunc(*args, **kwargs)
            cache[(i, Pai)] = score
            return score
