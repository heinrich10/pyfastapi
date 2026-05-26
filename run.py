import uvicorn
from uvicorn.config import LOGGING_CONFIG

from pyfastapi.utils.config import get_config
from pyfastapi.utils import configure_log
from pyfastapi import app

if __name__ == "__main__":
    config = get_config()
    uvicorn.run(app, host=config.HOST, port=config.PORT, log_config=configure_log(LOGGING_CONFIG))
