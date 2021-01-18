from simulatorTradingApi.seleniumUtil.HeadlessClient import HeadlessClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .Portfolio import UserPortfolio

import schedule
from threading import Thread, Event
from time import sleep

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

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.user = None

    def refreshSession(self):
        HeadlessClient.getInstance().refresh()

    def authenticate(self):
        if not self.isLoggedIn:
            client = HeadlessClient.getInstance()
            client.get("https://www.investopedia.com/simulator/home.aspx")
            client.save_screenshot("screenshot.png")
            loginButton = WebDriverWait(client, 10).until(
                EC.presence_of_element_located((By.ID, "login"))
            )
            username = client.find_element_by_id("username")
            password = client.find_element_by_id("password")
            username.send_keys(self.email)
            password.send_keys(self.password)
            loginButton.click()
            self.isLoggedIn = True
            thread = Thread(
                target=threaded_refresh, args=(HeadlessClient.getInstance(),)
            )
            thread.start()
            self.retrieveUserInfo()
        else:
            print("You are already authenticated.")

    def retrieveUserInfo(self):
        if not self.isLoggedIn:
            print("You need to login first.")
        else:
            client = HeadlessClient.getInstance()
            client.get("https://www.investopedia.com/simulator/portfolio/")
            self.user = UserPortfolio()

    def closeSession(self):
        HeadlessClient.close()
        print("Stopping thread from executing")
        exit_event.set()
        schedule.clear("refresh-task")

    def getAccountStatus(self):
        if not self.isLoggedIn:
            print("You need to login first.")
        else:
            return self.user.getPortfolio()

    def getHoldings(self):
        if not self.isLoggedIn:
            print("You need to login first.")
        else:
            return self.user.getHoldings()
