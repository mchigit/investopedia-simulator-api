from simulatorTradingApi.seleniumUtil.HeadlessClient import HeadlessClient
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UserPortfolio:
    def __init__(self):
        client = HeadlessClient.getInstance()
        info = client.find_elements_by_class_name('infobar-title')
        # for info_ele in info:
        #     accountValueUSD = info_ele.find_element_by_tag_name('p').find_element_by_css_selector(':nth-child(2)')
        #     self.accountValueUSD = accountValueUSD
        accountValueUSD = info[0].find_element_by_tag_name('p').find_element_by_css_selector(':nth-child(2)').get_attribute('innerText')
        self.accountValueUSD = accountValueUSD

class Account:
    isLoggedIn = False

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.user = None

    def authenticate(self):
        if not self.isLoggedIn:
                client = HeadlessClient.getInstance()
                client.get('https://www.investopedia.com/simulator/home.aspx')
                client.save_screenshot("screenshot.png")
                loginButton = WebDriverWait(client, 10).until(
                    EC.presence_of_element_located((By.ID, "login"))
                )
                username = client.find_element_by_id('username')
                password = client.find_element_by_id('password')
                username.send_keys(self.email)
                password.send_keys(self.password)
                loginButton.click()
                self.isLoggedIn = True
                self.retrieveUserInfo()
        else:
            print("You are already authenticated.")

    def retrieveUserInfo(self):
        if not self.isLoggedIn:
            print("You need to login first.")
        else:
            client = HeadlessClient.getInstance()
            client.get('https://www.investopedia.com/simulator/portfolio/')
            client.save_screenshot('portfolio.png')
            self.user = UserPortfolio()
            print("account value: ", self.user.accountValueUSD)

    def closeSession(self):
        HeadlessClient.close()
