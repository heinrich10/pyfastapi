from typing import Any, Dict


def configure_log(uvicorn_log_config: Dict[str, Any]) -> Dict[str, Any]:
    formatters = uvicorn_log_config['formatters']
    formatters['default']['fmt'] = '%(levelprefix)s [%(asctime)s] %(message)s'
    formatters['access']['fmt'] = '%(levelprefix)s [%(asctime)s] %(client_addr)s - "%(request_line)s" %(status_code)s'
    return uvicorn_log_config
