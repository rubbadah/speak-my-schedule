import json
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE_PATH = "./config/config.json"


class Config:
    def __init__(self):
        with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as file:
            self.config_data = json.load(
                file,
            )

    @property
    def api_url(self):
        """
        Returns:
            str: api_url
        """
        return self.config_data.get("api_url", "")
