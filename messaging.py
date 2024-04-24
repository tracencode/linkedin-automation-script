import time
import traceback

from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager, ChromeDriver
from selenium_stealth import stealth

from dotenv import load_dotenv
import os

load_dotenv()

class LinkedinScraper:
    def __init__(self) -> None:
        self.driver = self._get_driver()

    def _get_driver(self):
        ua = UserAgent()
        random_agent = ua.random
        fixed_agent = """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"""

        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")

        options.add_argument(f"user-agent={fixed_agent}")
        # options.add_argument(f"user-agent={random_agent}")
        options.add_argument("disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--incognito")
        # options.add_argument("--headless")

        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        stealth(
            driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        driver.implicitly_wait(4)
        driver.maximize_window()
        return driver

    def login(self, email: str, password: str):
        if not self.driver:
            return

        link = "https://www.linkedin.com/login"
        try:
            self.driver.get(link)
            self.driver.implicitly_wait(6)

            time.sleep(1)

            email_box = self.driver.find_element(By.XPATH, "//input[@id='username']")
            password_box = self.driver.find_element(By.XPATH, "//input[@id='password']")

            email_box.send_keys(email)
            time.sleep(1)
            password_box.send_keys(password)
            time.sleep(1)

            sign_in = self.driver.find_element(
                By.XPATH, '//*[@id="organic-div"]/form/div[3]/button'
            )
            sign_in.click()
            time.sleep(1)
        except Exception as e:
            print(traceback.format_exc())

    def send_message(self, recipient: str, message: str):
        if not self.driver:
            return

        link = "https://www.linkedin.com/messaging/thread/new/"
        try:
            self.driver.get(link)
            self.driver.implicitly_wait(6)

            time.sleep(3)

            search_name = self.driver.find_element(
                By.XPATH,
                '//input[contains(@class, "msg-connections-typeahead__search-field")]',
            )
            for name_part in recipient.split():
                search_name.send_keys(f"{name_part} ")
                time.sleep(1)
            time.sleep(2)

            search_name.send_keys(Keys.RETURN)
            message_box = self.driver.find_element(
                By.XPATH,
                '//form[contains(@class, "msg-form")]/div[3]/div/div[1]/div[1]/p',
            )
            message_box.send_keys(message)
            time.sleep(3)

            send_button = self.driver.find_element(
                By.XPATH,
                '//form[contains(@class, "msg-form")]/footer/div[2]/div[1]/button',
            )
            send_button.click()

            time.sleep(8)

        except Exception as e:
            print(traceback.format_exc())

    def logout(self):
        if not self.driver:
            return

        link = "https://www.linkedin.com/m/logout"
        try:
            self.driver.get(link)
            self.driver.implicitly_wait(4)
            time.sleep(4)
        except Exception as e:
            print(traceback.format_exc())



scraper = LinkedinScraper()

user_email = os.getenv('LINKEDIN_USER')
user_password = os.getenv('LINKEDIN_PASSWORD')
scraper.login(email=user_email, password=user_password)
scraper.send_message(recipient="Sandeep Singh Solanki", message="Hello !")
scraper.logout()