from simulatorTradingApi.seleniumUtil.HeadlessClient import HeadlessClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import pprint
import schedule
from threading import Thread, Event
from time import sleep

pp = pprint.PrettyPrinter(indent=4)

exit_event = Event()

def threaded_refresh(driver):
    def refresh():
        print("refreshing...")
        driver.refresh()
    schedule.every(10).seconds.do(refresh).tag('refresh-task')
    while 1:
        if not exit_event.is_set():
            schedule.run_pending()
            sleep(10)
        else:
            break

class UserPortfolio:
    def __init__(self):
        self.retrievePortfolio()

    def retrievePortfolio(self):
        client = HeadlessClient.getInstance()
        info = client.find_elements_by_class_name("infobar-title")

        if len(info) < 4:
            print("Failed to retrieve user portfolio")
            return

        accountValueUSD = (
            info[0]
            .find_element_by_tag_name("p")
            .find_element_by_css_selector(":nth-child(2)")
            .get_attribute("innerText")
        )
        buyingPower = (
            info[1]
            .find_element_by_tag_name("p")
            .find_element_by_css_selector(":nth-child(2)")
            .get_attribute("innerText")
        )

        cash = (
            info[2]
            .find_element_by_tag_name("p")
            .find_element_by_css_selector(":nth-child(2)")
            .get_attribute("innerText")
        )

        annualReturn = (
            info[3]
            .find_element_by_tag_name("p")
            .find_element_by_css_selector(":nth-child(2)")
            .get_attribute("innerText")
        )

        self.accountValueUSD = self.__extractNumber(accountValueUSD)
        self.buyingPower = self.__extractNumber(buyingPower)
        self.cash = self.__extractNumber(cash)
        self.annualReturn = self.__extractNumber(annualReturn)

    def __extractNumber(self, string):
        trimmed = string.strip()
        if "$" in trimmed:
            return float(trimmed[1:].replace(",", ""))
        else:
            return float(trimmed[:-1].replace(",", ""))


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
            thread = Thread(target=threaded_refresh, args=(HeadlessClient.getInstance(), ))
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
            client.save_screenshot("portfolio.png")
            self.user = UserPortfolio()
            pp.pprint(self.user.accountValueUSD)
            pp.pprint(self.user.buyingPower)
            pp.pprint(self.user.cash)
            pp.pprint(self.user.annualReturn)

    def closeSession(self):
        HeadlessClient.close()
        print("Stopping thread from executing")
        exit_event.set()
        schedule.clear('refresh-task')
