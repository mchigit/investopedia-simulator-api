from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ..config import DRIVER_PATH, USER_AGENT


class HeadlessClient:
    _instance = None

    def __init__(self):
        if HeadlessClient._instance != None:
            raise Exception("This class is a singleton!")
        else:
            chrome_options = Options()
            print(DRIVER_PATH)
            # chrome_options.headless = True
            chrome_options.add_argument("user-agent={}".format(USER_AGENT))
            chrome_options.add_argument("--incognito")
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--profile-directory=Default')
            chrome_options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(DRIVER_PATH, options=chrome_options)
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
