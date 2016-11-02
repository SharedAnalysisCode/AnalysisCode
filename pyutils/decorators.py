
#_____________________________________________________________________________
def save_runtime(func):
    """
    Decorator for saving runtime spent on a function.  You should use this to
    decorate the execute method of your Algorithms:
        
        @pyframe.core.save_runtime
        execute(self, weight):
            pass
    """
    def wrapper(*args, **kw):
        if not hasattr(wrapper, '_runtime'):
            wrapper._runtime = 0.0
            wrapper._n_calls = 0
        t1 = time.time()
        result = func(*args, **kw)
        t2 = time.time()
        wrapper._runtime += (t2-t1)
        wrapper._n_calls += 1
        return result
    return wrapper


#_____________________________________________________________________________
class memoized(object):
   """Decorator that caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned, and
   not re-evaluated.
   """
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      try:
         return self.cache[args]
      except KeyError:
         value = self.func(*args)
         self.cache[args] = value
         return value
      except TypeError:
         # uncachable -- for instance, passing a list as an argument.
         # Better to not cache than to blow up entirely.
         return self.func(*args)
   def __repr__(self):
      """Return the function's docstring."""
      return self.func.__doc__
   def __get__(self, obj, objtype):
      """Support instance methods."""
      return functools.partial(self.__call__, obj)

