# Caching Examples

Learn how to use EvolutePrompt's caching capabilities to improve efficiency and reduce API costs.

## Basic Caching

```python
from evoluteprompt import Cache, PromptBuilder
from evoluteprompt.cache import InMemoryCache, RedisCache

# Initialize an in-memory cache
cache = InMemoryCache()

# Create a provider with caching
provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    cache=cache
)

# Cached completions
prompt = PromptBuilder()\
    .add_user("What is the capital of France?")\
    .build()

# First call will hit the API
response1 = provider.complete(prompt)

# Second call will use cached result
response2 = provider.complete(prompt)  # Returns cached response
```

## Redis Caching

```python
# Initialize Redis cache
redis_cache = RedisCache(
    host="localhost",
    port=6379,
    ttl=3600  # Cache entries expire after 1 hour
)

provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    cache=redis_cache
)
```

## Advanced Caching Features

```python
from evoluteprompt.cache import CacheConfig, CacheKey

# Configure cache with custom settings
cache_config = CacheConfig(
    ttl=1800,  # 30 minutes
    max_size=1000,  # Maximum number of entries
    namespace="my_project"
)

cache = InMemoryCache(config=cache_config)

# Custom cache key generation
class CustomCacheKey(CacheKey):
    def generate(self, prompt, **kwargs):
        # Custom logic to generate cache key
        return f"{prompt.hash()}:{kwargs.get('temperature', 1.0)}"

# Use custom cache key
provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    cache=cache,
    cache_key_generator=CustomCacheKey()
)
```

## Cache Management

```python
# Clear specific entries
cache.delete("prompt_key")

# Clear namespace
cache.clear_namespace("my_project")

# Clear all cache
cache.clear()

# Get cache statistics
stats = cache.get_stats()
print(f"Cache hits: {stats.hits}")
print(f"Cache misses: {stats.misses}")
print(f"Cache size: {stats.size}")

# Cache with conditions
provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    cache=cache,
    cache_conditions={
        "temperature": lambda t: t == 0,  # Only cache deterministic responses
        "max_tokens": lambda t: t <= 100  # Only cache short responses
    }
)
```

## Distributed Caching

```python
from evoluteprompt.cache import DistributedCache

# Set up distributed cache
distributed_cache = DistributedCache(
    nodes=[
        {"host": "cache1.example.com", "port": 6379},
        {"host": "cache2.example.com", "port": 6379},
    ],
    replication_factor=2
)

# Use distributed cache
provider = OpenAIProvider(
    api_key="YOUR_API_KEY",
    cache=distributed_cache
)

# Cache synchronization
distributed_cache.sync()  # Ensure cache consistency across nodes
``` 