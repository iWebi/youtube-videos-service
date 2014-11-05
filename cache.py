from datetime import datetime

__author__ = 'suman'


class CacheElement(object):
    def __init__(self, date=None, data=None, duration_in_seconds=7200):  # 7200 = 2 hours in seconds
        self._date = date
        self._data = data
        self._duration = duration_in_seconds

    @property
    def duration_in_seconds(self):
        return self._duration

    @property
    def date(self):
        return self._date


class Cache(object):
    def __init__(self):
        self._cache = {}

    def add_to_cache(self, key, data, duration=7200):  # 7200 = 2 hours in seconds
        self._cache[key] = CacheElement(date=datetime.utcnow(), data=data, duration_in_seconds=duration)
        return data

    def get_from_cache(self, key):
        data = self._cache.get(key, None)
        if data:
            # TODO: add logging
            current_time = datetime.utcnow()
            cached_time = data.date
            elapsed_seconds = (current_time - cached_time).seconds
            if elapsed_seconds < data.duration_in_seconds:
                return data
            else:
                return None