from pyfastapi.utils import init_logger
# instantiate logger before anything else
init_logger()  # noqa: E402

from .main import app


__all__ = ["app"]
