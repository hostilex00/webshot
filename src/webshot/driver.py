from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def chrome() -> webdriver.Chrome:
    options = Options()
    options.add_argument('headless')
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    return driver