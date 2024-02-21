from pyfastapi.utils import init_logger
# instantiate logger before anything else
init_logger()

from .main import app


__all__ = ["app"]
