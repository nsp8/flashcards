import logging


BACKEND_API_URI = "http://127.0.0.1:8000"
STREAMLIT_APP_URI = "http://127.0.0.1:8501"


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(f"{name}.log")
        formatter = logging.Formatter(
            "%(asctime)s: " "%(levelname)s: " "[%(funcName)s] " "%(message)s"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
