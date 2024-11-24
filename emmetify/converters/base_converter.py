class BaseConverter:
    """Base interface for all converters"""
    def convert(self, nodes):
        raise NotImplementedError
