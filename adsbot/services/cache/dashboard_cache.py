# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
cache = {}


def get(user_id: int):
    return cache.get(user_id)


def set(user_id: int, value):
    cache[user_id] = value


def clear(user_id: int):
    cache.pop(user_id, None)