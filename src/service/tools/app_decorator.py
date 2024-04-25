
def authorized(method):
    def wrapper(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        
        
        return result
    return wrapper