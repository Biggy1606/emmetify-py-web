class BaseParser:
    """Base interface for all parsers"""
    def parse(self, content):
        raise NotImplementedError
