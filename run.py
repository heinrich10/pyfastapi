import uvicorn
from uvicorn.config import LOGGING_CONFIG

from pyfastapi.utils.config import get_config
from pyfastapi.utils import configure_log
from pyfastapi import app

Config = get_config()

if __name__ == "__main__":
    uvicorn.run(app, host=Config.HOST, port=Config.PORT, log_config=configure_log(LOGGING_CONFIG))
