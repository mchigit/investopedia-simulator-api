from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ..config import Config


class HeadlessClient:
    _instance = None

    def __init__(self):
        if HeadlessClient._instance != None:
            raise Exception("This class is a singleton!")
        else:
            chrome_options = Options()
            # chrome_options.headless = True
            chrome_options.add_argument("user-agent={}".format(Config.USER_AGENT))
            chrome_options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(Config.DRIVER_PATH, options=chrome_options)
            HeadlessClient._instance = driver

    @staticmethod
    def get_instance():
        if HeadlessClient._instance is None:
            HeadlessClient()
        return HeadlessClient._instance

    @staticmethod
    def close():
        if HeadlessClient._instance is None:
            print("Client is already closed")
        else:
            HeadlessClient._instance.close()
            HeadlessClient._instance = None
