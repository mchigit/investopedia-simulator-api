from simulatorTradingApi.seleniumUtil.HeadlessClient import HeadlessClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .Portfolio import UserPortfolio

import schedule
from threading import Thread, Event
from time import sleep

import logging
logging.basicConfig(level=logging.INFO)

exit_event = Event()


def threaded_refresh(driver):
    def refresh():
        print("refreshing...")
        driver.refresh()

    schedule.every(10).seconds.do(refresh).tag("refresh-task")
    while 1:
        if not exit_event.is_set():
            schedule.run_pending()
            sleep(10)
        else:
            break


class Account:
    isLoggedIn = False
    disableAutoRefresh = False
    __portfolio = None

    def __init__(self, email, password, disableAutoRefresh=False):
        self.email = email
        self.password = password
        self.disableAutoRefresh = disableAutoRefresh
        self.authenticate()

    def refreshSession(self):
        HeadlessClient.getInstance().refresh()

    def authenticate(self):
        try:
            client = HeadlessClient.getInstance()
            client.get("https://www.investopedia.com/simulator/home.aspx")
            loginButton = WebDriverWait(client, 10).until(
                EC.presence_of_element_located((By.ID, "login"))
            )
            username = client.find_element_by_id("username")
            password = client.find_element_by_id("password")
            username.send_keys(self.email)
            password.send_keys(self.password)
            loginButton.click()
            if not self.disableAutoRefresh:
                thread = Thread(target=threaded_refresh, args=(client,))
                thread.start()
            self.__portfolio = UserPortfolio()
            self.isLoggedIn = True
        except Exception as e:
            logging.error("Failed to login.", exc_info=True)
            self.closeSession()

    @staticmethod
    def closeSession(self):
        if Account.isLoggedIn:
            client = HeadlessClient.getInstance()
            client.get("https://www.investopedia.com/simulator/logout.aspx")
            HeadlessClient.close()
            exit_event.set()
            schedule.clear("refresh-task")

    def getPortfolio(self):
        if self.isLoggedIn:
            return self.__portfolio.getPortfolio()
        else:
            raise Exception("Please login first.")

    def getHoldings(self):
        if self.isLoggedIn:
            return self.__portfolio.getHoldings()
        else:
            raise Exception("Please login first.")
