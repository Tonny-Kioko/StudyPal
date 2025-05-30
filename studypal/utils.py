from django.conf import settings
import hashlib
from django.core.cache import cache

def generate_cache_key(view_name, identifier=None):

    cache_version = cache.get("cache_version", 1)
    key = f"{settings.CACHE_KEY_PREFIX}{view_name}_v{cache_version}"
    if identifier:
        key = f"{key}_{identifier}"
    return hashlib.md5(key.encode()).hexdigest()
