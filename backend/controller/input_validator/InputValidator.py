
class InputValidator:
    """ Base class for input validators. """
    def is_valid(self, data):
        """ Validate the input data. Should be overridden by subclasses. """
        if (data is None):
            return False