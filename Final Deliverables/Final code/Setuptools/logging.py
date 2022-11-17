import sys
import logging
import distutils.log
from . import monkey


def _not_warning(record):
    return record.levelno < logging.WARNING


def configure():
    """
    Configure logging to emit warning and above to stderr
    and everything else to stdout. This behavior is provided
    for compatibilty with distutils.log but may change in
    the future.
    """
    err_handler = logging.StreamHandler()
    err_handler.setLevel(logging.WARNING)
    out_handler = logging.StreamHandler(sys.stdout)
    out_handler.addFilter(_not_warning)
    handlers = err_handler, out_handler
    logging.basicConfig(
        format="{message}", style='{', handlers=handlers, level=logging.DEBUG)
    monkey.patch_func(set_threshold, distutils.log, 'set_threshold')


def set_threshold(level):
    logging.root.setLevel(level*10)
    return set_threshold.unpatched(level)