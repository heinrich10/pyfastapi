import sys
import logging
from typing import Any, Dict
from uvicorn.logging import ColourizedFormatter

# toggle between info and debug
LOG_LEVEL = logging.INFO
# LOG_LEVEL = logging.DEBUG


def init_logger():
    """
    Initialize logger, has to be run first above all
    """
    formatter = ColourizedFormatter(fmt='%(levelprefix)s [%(asctime)s] %(name)s - %(message)s', use_colors=True)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logging.basicConfig(
        level=LOG_LEVEL,
        handlers=[handler]
    )


def configure_log(uvicorn_log_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Configure log of uvicorn
    Get the default uvicorn_log_config and then override the formatter
    """
    formatters = uvicorn_log_config['formatters']
    formatters['default']['fmt'] = '%(levelprefix)s [%(asctime)s] %(message)s'
    formatters['access']['fmt'] = '%(levelprefix)s [%(asctime)s] %(client_addr)s - "%(request_line)s" %(status_code)s'
    return uvicorn_log_config
