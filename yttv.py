from selenium import webdriver
from selenium.webdriver.common.by import By

import time

USER_AGENT = 'Mozilla/5.0 (SMART-TV; Linux; Tizen 4.0.0.2) AppleWebkit/605.1.15 (KHTML, like Gecko) SamsungBrowser/9.2 TV Safari/605.1.15'
SCRIPT_BLOCKER = 'uBlock0_1.42.4.firefox.signed.xpi'

if __name__ == '__main__':
    # Configure Browser
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")
    # Configure Profile
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", USER_AGENT)

    driver = webdriver.Firefox(options=options, firefox_profile=profile)
    driver.install_addon(SCRIPT_BLOCKER, temporary=True)

    # Loading
    driver.get('https://www.youtube.com/tv#/')
    print("LOADING..")
    for i in range(3):
        print(i)
        time.sleep(1)

    # Go to Settings
    button = driver.find_element(By.CLASS_NAME, 'ytlr-icon--gear')
    print("Go to Settings")
    button.click()
    for i in range(2):
        print(i)
        time.sleep(1)
    print("Settings")

    # Go to Link with TV Code
    buttons = driver.find_elements(By.CLASS_NAME, 'yt-virtual-list__item')
    for button in buttons:
        if button.text == 'Link with TV code':
            print("Go to Link with TV Code")
            button.click()
            for i in range(2):
                print(i)
                time.sleep(1)
            print("Link with Wi-Fi")

    # Get TV Code
    print("Get TV Code")
    code = driver.find_element(By.CLASS_NAME, 'ytlr-link-phone-with-tv-code-renderer__pairing-code-text')
    print(code.text)

    # Screenshot
    print("Screenshot")
    webpage = driver.find_element(By.TAG_NAME, "body")
    webpage.screenshot('page.png')

    print('STARTED..')
    while True:
        time.sleep(1)
    # Postprocess
    # driver.quit()
