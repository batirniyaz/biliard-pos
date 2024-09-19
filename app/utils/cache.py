from fastapi_cache.backends.inmemory import InMemoryBackend


class InMemoryCacheBackend(InMemoryBackend):
    def __init__(self):
        super().__init__()
        self.cache = {}

    async def get(self, key: str):
        return self.cache.get(key)

    async def set(self, key: str, value: str, expire: int = None):
        self.cache[key] = value

    async def clear(self):
        self.cache.clear()
