import uvicorn

from pyfastapi.config import Config
from pyfastapi.main import app


if __name__ == "__main__":
    uvicorn.run(app, host=Config.HOST, port=Config.PORT, log_level=Config.LOG_LEVEL)
