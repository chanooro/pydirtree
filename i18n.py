from pathlib import Path
import json

_LOCALES_DIR = Path(__file__).with_name("locales")
_FALLBACK = "en"
_cache = {}

def load_lang(lang: str):
    lang = (lang or _FALLBACK).lower()
    path = _LOCALES_DIR / f"{lang}.json"
    fb   = _LOCALES_DIR / f"{_FALLBACK}.json"
    data = {}
    if fb.exists():
        data.update(json.loads(fb.read_text(encoding="utf-8")))
    if path.exists():
        data.update(json.loads(path.read_text(encoding="utf-8")))
    _cache[lang] = data
    return data

def t(key: str, lang: str):
    d = _cache.get(lang) or load_lang(lang)
    return d.get(key, key)
