from selenium import webdriver
from time import sleep


def get_page(link, time_sleep = 10):
    # Use Selenium because requests cannot see the JavaScript-loaded restaurants.
    driver = webdriver.Chrome()
    driver.get(link)
    sleep(time_sleep)
    page = driver.page_source
    driver.close()

    return page