from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ..config import config


class HeadlessClient:
    _instance = None

    def __init__(self):
        if HeadlessClient._instance != None:
            raise Exception("This class is a singleton!")
        else:
            chrome_options = Options()
            # chrome_options.headless = True
            chrome_options.add_argument("user-agent={}".format(config.USER_AGENT))
            chrome_options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(config.DRIVER_PATH, options=chrome_options)
            HeadlessClient._instance = driver

    @staticmethod
    def getInstance():
        if HeadlessClient._instance == None:
            HeadlessClient()
        return HeadlessClient._instance

    @staticmethod
    def close():
        if HeadlessClient._instance == None:
            print("Client is already closed")
        else:
            HeadlessClient._instance.close()
            HeadlessClient._instance = None
