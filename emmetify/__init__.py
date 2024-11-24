from emmetify.emmetifier import Emmetifier
from emmetify.config import __all__ as config_all


def emmetify(content, format="html", **options):
    """Convenience function for quick conversions"""
    emmetifier = Emmetifier(format=format, **options)
    return emmetifier.emmetify(content)


__all__ = [
    "Emmetifier",
    "emmetify",
    *config_all,
]
