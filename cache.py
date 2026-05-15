import json
import os

CACHE_FILE = "email_cache.json"

def load_cache() -> dict:
    if not os.path.exists(CACHE_FILE):
        return{}
    with open(CACHE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_cache(cache: dict):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def get_cached_analysis(email_id: str) -> dict | None:
    cache = load_cache()

    return cache.get(email_id, None)

def save_analysis(email_id: str, analysis: dict):
    cache = load_cache()
    cache[email_id] = analysis
    save_cache(cache)