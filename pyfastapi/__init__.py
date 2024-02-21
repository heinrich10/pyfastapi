from pyfastapi.utils import init_logger
# instantiate logger before anything else
init_logger()

from .main import app  # noqa: E402


__all__ = ["app"]
