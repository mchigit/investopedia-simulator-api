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
    is_logged_in = False
    disable_auto_refresh = False
    __portfolio = None

    def __init__(self, email, password, disable_auto_refresh=False):
        self.email = email
        self.password = password
        self.disable_auto_refresh = disable_auto_refresh
        self.authenticate()

    def refresh_session(self):
        HeadlessClient.get_instance().refresh()

    def authenticate(self):
        try:
            client = HeadlessClient.get_instance()
            client.get("https://www.investopedia.com/simulator")
            login = WebDriverWait(client, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='Log In']"))
            )
            login.click()
            
            WebDriverWait(client, 10).until(
                EC.presence_of_element_located((By.ID, "login"))
            )
            username = client.find_element_by_id("username")
            password = client.find_element_by_id("password")
            username.send_keys(self.email)
            password.send_keys(self.password)
            
            client.find_element_by_css_selector("form").submit()
            
            if not self.disable_auto_refresh:
                thread = Thread(target=threaded_refresh, args=(client,))
                thread.start()
            WebDriverWait(client, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "sim-page"))
            )
            self.__portfolio = UserPortfolio()
            self.is_logged_in = True
        except Exception as e:
            logging.error("Failed to login.", exc_info=True)
            self.close_session

    def close_session(self):
        client = HeadlessClient.get_instance()
        client.get("https://www.investopedia.com/simulator/logout.aspx")
        HeadlessClient.close()
        exit_event.set()
        schedule.clear("refresh-task")

    def get_portfolio(self):
        if self.is_logged_in:
            return self.__portfolio.get_portfolio()
        else:
            raise Exception("Please login first.")

    def get_holdings(self):
        if self.is_logged_in:
            return self.__portfolio.get_holdings()
        else:
            raise Exception("Please login first.")
