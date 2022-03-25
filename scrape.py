from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

def americanToDecimal(a):
    if not a: return None
    sign = a[0]
    if sign == "+":
        return 1 + int(a[1:]) / 100 
    elif sign == "-":
        return 1 + 100 / int(a[1:])
    else:
        return None

def scrapeBet365(d):
    d.get("https://www.bet365.com/#/AC/B17/C20798172/D48/E972/F10/")
    time.sleep(1)
    element = WebDriverWait(d, 8).until(EC.presence_of_element_located((By.CLASS_NAME, 'gl-MarketGroupContainer')))
    teams = element.find_elements(by=By.XPATH, value='//div[@class="sci-ParticipantFixtureDetailsHigherIceHockey_Team "]')
    money_line = element.find_elements(by=By.XPATH, value='//span[@class="sac-ParticipantOddsOnly50OTB_Odds"]')
    bet365 = {}
    for i in range(len(teams)):
        odds = americanToDecimal(money_line[i].text)
        if odds:
            bet365[teams[i].text] = odds
    return bet365

def scrapeBetway(d):    
    d.get("https://betway.com/en/sports/grp/ice-hockey/north-america/nhl")
    time.sleep(1)
    element = WebDriverWait(d, 8).until(EC.presence_of_element_located((By.CLASS_NAME, 'eventItemCollection')))
    events = element.find_elements(by=By.XPATH, value='//div[@class="oneLineEventItem"]')
    betway = {}
    for i in range(len(events)):
        text = events[i].text.split("\n")
        print(text)
    return betway

# chromedriver setup 
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)


# print(scrapeBet365(driver))
print(scrapeBetway(driver))





