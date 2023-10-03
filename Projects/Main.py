from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import os.path
import sys
import TestFlowRekapitulasiBerjenjang
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
    
def setup_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--incognito")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("disable-infobars")

    options.add_experimental_option("prefs",{'credentials_enable_service': False, 'profile': {'password_manager_enabled': False}})
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    return driver

def execute_script_click(driver, locator):
    element = driver.find_element(*locator)
    driver.execute_script("arguments[0].click();", element)

def webdriver_wait_hidden(driver, time, locator):
    element_present = WebDriverWait(driver, time).until(EC.presence_of_element_located(locator))
    return element_present

def webdriver_wait(driver, time, locator):
    element_present = WebDriverWait(driver, time).until(EC.visibility_of_element_located(locator))
    return element_present

def webdriver_wait_many(driver, time, locator):
    elements = WebDriverWait(driver, time).until(EC.presence_of_all_elements_located(locator))
    visible_elements = [element for element in elements if element.is_displayed()]
    return visible_elements

def main():
    driver = setup_webdriver()
    TestFlowRekapitulasiBerjenjang.main(driver)


if __name__ == '__main__':
    main()
    k = input("\nPress enter to exit...")