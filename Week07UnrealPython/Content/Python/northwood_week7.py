"""Compatibility for earlier Week 7 notes. New code should import week07_tools."""
import week07_tools as _tools


def __getattr__(name):
    return getattr(_tools, name)


def __dir__():
    return sorted(set(globals()) | set(dir(_tools)))
