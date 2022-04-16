import logging
logging.getLogger().setLevel(logging.INFO)

import os
import time
import urllib.request

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

USER_AGENT = 'Mozilla/5.0 (SMART-TV; Linux; Tizen 4.0.0.2) AppleWebkit/605.1.15 (KHTML, like Gecko) SamsungBrowser/9.2 TV Safari/605.1.15'
SCRIPT_BLOCKER_VERSION = '1.42.4'
SCRIPT_BLOCKER = 'uBlock0_' + SCRIPT_BLOCKER_VERSION + '.firefox.signed.xpi'
SCRIPT_BLOCKER_URL = 'https://github.com/gorhill/uBlock/releases/download/' + SCRIPT_BLOCKER_VERSION + '/' + SCRIPT_BLOCKER
FIREFOX_BIN = r'/opt/firefox/firefox'


class YTTV:

    def __init__(self):
        PROFILE_DIRECTORY = '.yttv_config/firefox_profile'
        os.makedirs(PROFILE_DIRECTORY, exist_ok=True)
        # Configure Browser
        options = webdriver.FirefoxOptions()
        options.binary = FirefoxBinary(FIREFOX_BIN)
        options.add_argument("--headless")
        profile = webdriver.FirefoxProfile(profile_directory=PROFILE_DIRECTORY)
        profile.set_preference("general.useragent.override", USER_AGENT)

        self.driver = webdriver.Firefox(options=options,
                                        firefox_profile=profile)
        self.driver.delete_all_cookies()
        self.install_no_script()

    def install_no_script(self):
        urllib.request.urlretrieve(SCRIPT_BLOCKER_URL, SCRIPT_BLOCKER)
        self.driver.install_addon(SCRIPT_BLOCKER, temporary=True)

    def stop_app(self):
        self.driver.quit()

    def get_settings_tv_code(self) -> str:
        # Go to Settings
        button = self.driver.find_element(By.CLASS_NAME, 'ytlr-icon--gear')
        logging.info("Go to Settings")
        button.click()
        for idx in range(5):
            logging.info(str(idx))
            time.sleep(1)
        logging.info("Settings")
        # Go to Link with TV Code
        buttons = self.driver.find_elements(By.CLASS_NAME,
                                            'yt-virtual-list__item')
        for button in buttons:
            if button.text == 'Link with TV code':
                logging.info("Go to Link with TV Code")
                button.click()
                for idx in range(5):
                    logging.info(str(idx))
                    time.sleep(1)
                logging.info("Link with Wi-Fi")
        # Get TV Code
        logging.info("Get TV Code")
        code = self.driver.find_element(By.CLASS_NAME,
                                        'ytlr-link-phone-with-tv-code-renderer__pairing-code-text')
        logging.info(code.text)
        return code.text.replace(' ', '')

    def load_app(self):
        # Loading
        self.driver.get('https://www.youtube.com/tv')
        logging.info("LOADING..")
        for i in range(5):
            logging.info(str(i))
            time.sleep(1)

    def reset_app(self):
        logging.info("RESET..")
        running = True
        i = 0
        while running:
            webdriver.ActionChains(self.driver).send_keys(
                Keys.ESCAPE).perform()
            for z in range(5):
                logging.info(str(z))
                time.sleep(z)
            elements = self.driver.find_elements(By.TAG_NAME,
                                                 'ytlr-button-renderer')
            logging.info(i)
            i = + 1
            if len(elements) == 2:
                for element in elements:
                    if element.text == 'CANCEL':
                        running = False
                        element.click()
                        time.sleep(1)
                        break


if __name__ == '__main__':
    yttv = YTTV()
    try:
        yttv.load_app()
        tv_code = yttv.get_settings_tv_code()
        while True:
            time.sleep(1)
    except Exception as e:
        logging.info(e)
        yttv.stop_app()
    yttv.stop_app()
