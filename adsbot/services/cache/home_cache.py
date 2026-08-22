# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
cache = {}


def get(page: str):

    return cache.get(page)


def set(page: str, value):

    cache[page] = value


def clear():

    cache.clear()