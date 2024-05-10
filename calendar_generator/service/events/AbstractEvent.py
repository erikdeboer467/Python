from abc import ABC, abstractmethod
from datetime import date
from typing import Callable, List

cache = {}

class AbstractEvent(ABC):
    def __init__(self, name, isValid: Callable[[date], bool] = lambda d: True):
        self.name = name
        self.isValid = isValid

    @abstractmethod
    def get_date(self, year) -> date:
        pass

    def cached(self, keys: List[int], get: Callable[[], date] ) -> date:
        key = '-'.join([str(e) for e in keys])
        if not key in cache:
            cache[key] = get()

        return cache[key]
