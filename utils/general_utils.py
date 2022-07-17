
def singleton(cls):
    """
    Decorator to make a class a singleton.
    """
    instances = {}
    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _singleton