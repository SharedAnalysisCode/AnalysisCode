
import re

class redict(dict):
    def __init__(self):
        self.ordered_keys = []
        super(redict, self).__init__()

    def __setitem__(self, key, item):
        self.ordered_keys.append(key)
        super(redict, self).__setitem__(key, item)

    def matches(self, pattern):
        """
        Returns a list of the values for which the corresponding keys match pattern.
        """
        _matches = []
        for key in self.ordered_key:
            if re.match(pattern, key):
                _matches.append( self.get(key) )
        return _matches

    def match(self, pattern):
        """
        Returns the last value matching the pattern, preferring the latest match
        added to the dictionary.
        """
        _matches = self.matches(pattern)
        if _matches:
            return _matches[-1] # give preference to the last match
        else:
            return None

    def rules(self, word):
        """
        Returns a list of the values which have a key that is a pattern matching
        word.
        """
        _matches = []
        for key in self.ordered_keys:
            if re.match(key, word):
                _matches.append( self.get(key) )
        return _matches

    def rule(self, word):
        """
        Returns the value whose key is a pattern matching word, preferring the
        latest match added to the dictionary.
        """
        _matches = self.rules(word)
        if _matches:
            return _matches[-1] # give preference to the last rule
        else:
            return None




