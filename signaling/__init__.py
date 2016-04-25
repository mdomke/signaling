from pkg_resources import get_distribution

from signaling.signal import Signal


def version():
    return get_distribution(__name__).version


__version__ = version()
__all__ = ['Signal']
