class lookahead():
     "Wrap iterator with lookahead to both peek and test exhausted"

     _NONE = object()
     def __init__(self, iterable):
         self._it = iter(iterable)
         self._set_peek()
     def __iter__(self):
         return self
     def __next__(self):
         if self:
             ret = self.peek
             self._set_peek()
             return ret
         else:
             raise StopIteration()
     def _set_peek(self):
         try:
             self.peek = next(self._it)
         except StopIteration:
             self.peek = self._NONE
     def __nonzero__(self):
         return self.peek is not self._NONE

     def next(self):
         return self.__next__();

