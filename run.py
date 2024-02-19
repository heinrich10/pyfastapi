import uvicorn

from pyfastapi.config import get_config
from pyfastapi.main import app

Config = get_config()

if __name__ == "__main__":
    uvicorn.run(app, host=Config.HOST, port=Config.PORT, log_level=Config.LOG_LEVEL)
