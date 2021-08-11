from dotenv import dotenv_values
import os

config = dotenv_values(".env")
# print(config)

def get_env(key):
    return os.environ.get(key) or config.get(key)
