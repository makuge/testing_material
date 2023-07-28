import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


def test_inner_find():
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    try:
        driver.get("file:///C:/Temp/testing_material/selenium/example.html")

        elements = driver.find_elements(By.CSS_SELECTOR, "ul>li")

        result = {}

        for element in elements:
            h1_text = element.find_element(By.CSS_SELECTOR, "h1").text
            p_text = element.find_element(By.CSS_SELECTOR, "p").text
            result[h1_text] = p_text

        # result enthält jetzt {'1': 'a', '2': 'b', '3': 'c'}

        time.sleep(5)

    finally:
        driver.quit()
