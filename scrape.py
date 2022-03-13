from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)
driver.get("https://betway.com/en/sports/grp/ice-hockey/north-america/nhl")
element = WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.CLASS_NAME, 'eventItemCollection')))

events = element.find_elements(by=By.XPATH, value='//div[@class="oneLineEventItem"]')
event_list = []
for i in range(len(events)):
    event_list.append(events[i].text)

print(event_list)

