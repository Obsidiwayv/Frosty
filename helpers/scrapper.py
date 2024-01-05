import platform
import utils

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options

config = utils.get_config()


def scrape_website(url: str):
    # Specify the path to your Firefox binary
    firefox_binary_path = config["firefox"]["windows"] if platform.system() == 'Windows' \
        else config["firefox"]["linux"]

    # Set up the Firefox webdriver with options
    firefox_options = Options()
    firefox_options.headless = True  # Run Firefox in headless mode (without opening a browser window)

    # Provide the path to your geckodriver executable
    geckodriver_path = config["gecko"]["windows"] if platform.system() == 'Windows' \
        else config["gecko"]["linux"]
    service = FirefoxService(executable_path=geckodriver_path)

    # Use the custom Firefox binary
    firefox_options.binary_location = firefox_binary_path

    # Launch the Firefox browser
    driver = webdriver.Firefox(service=service, options=firefox_options)

    # Load the page
    driver.get(url)

    return driver
